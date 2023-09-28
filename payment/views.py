import base64

from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotAcceptable

from socketio import AsyncServer

from beelearn.asgi import sio

from .models import Purchase
from .serializers import PurchaseSerializer
from .googleplay import googleplay
from .googleplay_type import (
    TypePlaystoreWebhookMessage,
    TypePlaystoreWebhookMessageData,
    TypeSubscriptionState,
)

sio: AsyncServer = sio


class WebhookAPIView(APIView):
    @action(["POST"], url_name="flutterwave")
    def flutterwave_webhook(request: Request):
        # todo implement flutterwave webhook handler
        return Response()

    @action(["POST"], url_name="googleplay")
    def googleplay_store_webhook(request: Request):
        """
        googleplay webhook notification listener
        """
        messsage: TypePlaystoreWebhookMessage | None = request.data.get("message")

        if messsage:
            data = messsage.get("data")
            if data:
                data: TypePlaystoreWebhookMessageData = base64.b64decode(data)
                subscriptionNotification = data.get("subscriptionNotification")
                oneTimeSubscriptionNotification = data.get("oneTimeProductNotification")

                if subscriptionNotification:
                    purchase = get_object_or_404(
                        Purchase,
                        reference=subscriptionNotification["purchaseToken"],
                    )
                    subscription = googleplay.purchase.subscription.get(
                        data["packageName"],
                        subscriptionNotification["purchaseToken"],
                    )

                    subscriptionState = subscription["subscriptionState"]

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

                    elif subscriptionState in [
                        TypeSubscriptionState.SUBSCRIPTION_STATE_CANCELED,
                        TypeSubscriptionState.SUBSCRIPTION_STATE_EXPIRED,
                        TypeSubscriptionState.SUBSCRIPTION_STATE_ON_HOLD,
                    ]:
                        purchase.status = Purchase.Status.PENDING
                    else:
                        purchase.status = Purchase.Status.UNKNOWN

                    purchase.save(update_fields=["status"])

                    return Response(
                        {
                            "status": "successful",
                            "message": "purchase status updated successfully",
                            "data": PurchaseSerializer(purchase).data,
                        }
                    )

                if oneTimeSubscriptionNotification:
                    pass

        raise NotAcceptable(
            "event not acceptable, event schema not able to be processed"
        )
