from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Literal, Tuple, TypedDict

from googleapiclient.errors import HttpError

from rest_framework import status
from rest_framework.exceptions import (
    NotFound,
    APIException,
    ValidationError,
    NotAcceptable,
)

from account.models import User
from .googleplay import googleplay
from .googleplay_type import TypeSubscriptionState
from .models import Product, Purchase


def _transfrom_googleapi_error(error: HttpError):
    exception_class = APIException

    if error.status_code == status.HTTP_404_NOT_FOUND:
        exception_class = NotFound
    if error.status_code == status.HTTP_400_BAD_REQUEST:
        exception_class = ValidationError

    return exception_class(
        {
            "reason": error.reason,
            "details": error.error_details,
        }
    )


class TypeProduct(TypedDict):
    productId: str
    purchaseId: str
    androidPackageId: str


class InAppPurchaseHandler(ABC):
    @staticmethod
    def verifySubscription(
        user: User, product: TypeProduct, token: str
    ) -> Tuple[Purchase, bool]:
        raise NotImplementedError()

    @staticmethod
    def verifyNonSubscription(
        user: User, product: TypeProduct, token: str
    ) -> Tuple[Purchase, bool]:
        raise NotImplementedError()


class GooglePlayInAppPurchaseHandler(InAppPurchaseHandler):
    @staticmethod
    def verifySubscription(user: User, product: TypeProduct, token: str):
        try:
            response = googleplay.purchase.subscription.get(
                product["androidPackageId"],
                token,
            )
            dbProduct = Product.objects.get(id=product["productId"])
            if response["subscriptionState"] in [
                TypeSubscriptionState.SUBSCRIPTION_STATE_ACTIVE.value,
                TypeSubscriptionState.SUBSCRIPTION_STATE_IN_GRACE_PERIOD.value,
            ]:
                print(product["purchaseId"])
                return Purchase.objects.update_or_create(
                    user=user,
                    product=dbProduct,
                    defaults={
                        "token": token,
                        "id": product["purchaseId"],
                        "status": Purchase.Status.SUCCESSFUL,
                    },
                )

            raise ValidationError(
                {
                    "subscription": response,
                    "reason": "subscription state is invalid %s "
                    % response["subscriptionState"],
                }
            )

        except HttpError as error:
            raise _transfrom_googleapi_error(error)
        except Exception as error:
            raise APIException(str(error))

    @staticmethod
    def verifyNonSubscription(user: User, product: TypeProduct, token: str):
        try:
            response = googleplay.purchase.product.get(
                token=token,
                productId=product["productId"],
                packageName=product["androidPackageId"],
            )

            product = Product.objects.get(id=product["productId"])

            if response["purchaseState"] == 2:
                return Purchase.objects.update_or_create(
                    user=user,
                    status=Purchase.Status.SUCCESSFUL,
                    token=response["purchaseToken"],
                    defaults={
                        "id": product["purchaseId"],
                    },
                )

        except HttpError as error:
            raise _transfrom_googleapi_error(error)
        except Exception as error:
            raise APIException(str(error))


class AppleInAppPurchaseHandler(InAppPurchaseHandler):
    @staticmethod
    def verifySubscription(user: User, product: TypeProduct, token: str):
        raise NotImplementedError()

    @staticmethod
    def verifyNonSubscription(user: User, product: TypeProduct, token: str):
        raise NotImplementedError()


class TypePurchaseData(TypedDict):
    token: str
    product: TypeProduct
    type: Literal["consumable", "nonconsumable"]
    source: Literal["apple_store", "google_play"]


class InAppPurchase:
    @staticmethod
    def verify(user: User, data: TypePurchaseData):
        """
        verify inapp purchase and subscriptions
        `raise NotAcceptable | ValidationError`
        """
        source = data["source"]
        handler: InAppPurchaseHandler | None = None

        match source:
            case "apple_store":
                handler = AppleInAppPurchaseHandler
            case "google_play":
                handler = GooglePlayInAppPurchaseHandler
            case _:
                raise NotAcceptable(
                    {
                        "reason": "%s source is not acceptable try another e.g google_play, apple_store"
                    }
                )

        if data["type"] == "consumable":
            return handler.verifySubscription(
                user,
                data["product"],
                data["token"],
            )
        elif data["type"] == "nonconsumable":
            return handler.verifyNonSubscription(
                user,
                data["product"],
                data["token"],
            )

        raise NotAcceptable(
            {
                "reason": "%s type is not a valid product type" % data["type"],
            }
        )
