import base64
import json
from typing import Dict, Literal

from django.http.response import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from socketio import AsyncServer
from account.models import User

from beelearn.asgi import sio

from .models import Product, Purchase
from .serializers import PurchaseSerializer
from .googleplay import googleplay
from .googleplay_type import (
    TypePlaystoreWebhookMessage,
    TypePlaystoreWebhookMessageData,
    TypeSubscriptionState,
)

sio: AsyncServer = sio


@api_view(["POST"])
def flutterwave_webhook(request: Request):
    # todo implement flutterwave webhook handler
    print(json.loads(request.body))
    return Response()


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def paystack_webhook(request: Request):
    # todo implement flutterwave webhook handler
    data = request.data

    event = data["event"]
    data = data["data"]

    match event:
        case "subscription.create":
            user = get_object_or_404(User, email=data["customer"]["email"])
            product = Product.objects.get(paystack_plan_code=data["plan"]["plan_code"])
            purchase, _ = Purchase.objects.get_or_create(
                user=user,
                product=product,
                order_id=None,
            )
            purchase.web_order_id = data["subscription_code"]
            purchase.save(update_fields=["web_order_id"])

        case "subscription.not_renew" | "subscription.failed" | "subscription.disabled":
            purchase = get_object_or_404(
                Purchase,
                web_order_id=data["subscription_code"],
                product__paystack_plan_code=data["plan"]["plan_code"],
            )

            purchase.status = (
                Purchase.Status.FAILED
                if event == "failed"
                else Purchase.Status.CANCELED
            )
        case "charge.success":
            user = get_object_or_404(User, email=data["customer"]["email"])
            product = Product.objects.get(paystack_plan_code=data["plan"]["plan_code"])
            purchase, _ = Purchase.objects.get_or_create(
                user=user,
                product=product,
                order_id=None,
            )

            purchase.status = Purchase.Status.SUCCESSFUL
            purchase.save(update_fields=["status"])

    return Response(
        {
            "status": "successful",
            "message": "webhook event successful",
        }
    )


@csrf_exempt
def googleplay_store_webhook(request: HttpRequest):
    """
    googleplay webhook notification listener
    """
    payload: Dict[Literal["message"], TypePlaystoreWebhookMessage] = json.loads(
        request.body
    )
    messsage = payload.get("message")

    if messsage:
        data = messsage.get("data")
        if data:
            data: TypePlaystoreWebhookMessageData = json.loads(
                base64.b64decode(data).decode("utf-8")
            )
            print(data)
            testNotification = data.get("testNotification")
            subscriptionNotification = data.get("subscriptionNotification")
            oneTimeSubscriptionNotification = data.get("oneTimeProductNotification")

            if subscriptionNotification:
                subscription = googleplay.purchase.subscription.get(
                    data["packageName"],
                    subscriptionNotification["purchaseToken"],
                )
                subscriptionState = subscription["subscriptionState"]

                product = get_object_or_404(
                    Product,
                    consumable=False,
                    id=subscriptionNotification["subscriptionId"],
                )
                purchase, _ = Purchase.objects.get_or_create(
                    product=product,
                    token=subscriptionNotification["purchaseToken"],
                )

                if (
                    subscriptionState
                    == TypeSubscriptionState.SUBSCRIPTION_STATE_PENDING
                ):
                    purchase.status = Purchase.Status.PENDING
                elif subscriptionState in [
                    TypeSubscriptionState.SUBSCRIPTION_STATE_ACTIVE,
                    TypeSubscriptionState.SUBSCRIPTION_STATE_IN_GRACE_PERIOD,
                ]:
                    purchase.status = Purchase.Status.SUCCESSFUL
                    if (
                        subscriptionState
                        == TypeSubscriptionState.SUBSCRIPTION_STATE_ACTIVE
                    ):
                        googleplay.purchase.subscription.acknowledge(
                            "com.oasis.beelearn",
                            subscriptionId=subscriptionNotification["subscriptionId"],
                            token=subscriptionNotification["purchaseToken"],
                        )
                elif subscriptionState in [
                    TypeSubscriptionState.SUBSCRIPTION_STATE_CANCELED,
                    TypeSubscriptionState.SUBSCRIPTION_STATE_EXPIRED,
                    TypeSubscriptionState.SUBSCRIPTION_STATE_ON_HOLD,
                ]:
                    purchase.status = Purchase.Status.CANCELED
                else:
                    purchase.status = Purchase.Status.UNKNOWN

                purchase.order_id = subscription["latestOrderId"]
                purchase.save(update_fields=["status", "order_id"])

                return JsonResponse(
                    {
                        "status": "successful",
                        "message": "purchase status updated successfully",
                        "data": PurchaseSerializer(purchase).data,
                    }
                )

            if oneTimeSubscriptionNotification:
                pass

            if testNotification:
                return JsonResponse(
                    {
                        "status": "successful",
                        "message": "test message received",
                    }
                )

    raise HttpResponseNotAllowed(
        "event not acceptable, event schema not able to be processed"
    )
