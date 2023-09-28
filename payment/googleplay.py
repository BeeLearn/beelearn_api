from typing import Dict, List, Literal, Dict, Optional

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from beelearn.settings import BASE_DIR

from .googleplay_type import (
    TypeAcknowlegementState,
    TypeRegionVerion,
    TypeSubscription,
    TypeSubscriptionState,
    TypeSubscriptionPurchase,
)


class GooglePlay:
    def __init__(self, credentials: Credentials):
        self.credientials = credentials
        self.purchase = GooglePlayPurchase(credentials)
        self.monetization = GooglePlayMonetization(credentials)


class GooglePlayMonetization:
    def __init__(self, credentials: Credentials):
        self.subscriptions = GooglePlayMonetizationSubscription(credentials)


class GooglePlayPublisherService:
    def __init__(self, credentials: Credentials):
        self.service = build(
            "androidpublisher",
            "v3",
            credentials=credentials,
        )


class GooglePlayMonetizationSubscription(GooglePlayPublisherService):
    def list(
        self,
        packageName: str,
        pageSize: Optional[int] = 50,
        pageToken: Optional[str] = None,
        showArchived: Optional[bool] = False,
    ) -> Dict[Literal["subscriptions"], List[TypeSubscription]]:
        return (
            self.service.monetization()
            .subscriptions()
            .list(
                packageName=packageName,
                pageSize=pageSize,
                pageToken=pageToken,
                showArchived=showArchived,
            )
            .execute()
        )

    def get(self, packageName: str, productId: str) -> TypeSubscription:
        return (
            self.service.monetization()
            .subscriptions()
            .get(
                packageName=packageName,
                productId=productId,
            )
            .execute()
        )

    def create(
        self,
        packageName: str,
        productId: str,
        regionsVersion: TypeRegionVerion,
        body: TypeSubscription,
    ) -> TypeSubscription:
        request = (
            self.service.monetization()
            .subscriptions()
            .create(
                packageName=packageName,
                productId=productId,
                body=body,
            )
        )

        request.uri += "&regionsVersion.version=%s" % regionsVersion["version"]

        return request.execute()

    def patch(
        self,
        packageName: str,
        productId: str,
        updateMask: str,
        regionsVersion: TypeRegionVerion,
        body: TypeSubscription,
    ) -> TypeSubscription:
        request = (
            self.service.monetization()
            .subscriptions()
            .patch(
                productId=productId,
                updateMask=updateMask,
                packageName=packageName,
                body=body,
            )
        )
        request.uri += "&regionsVersion.version=%s" % regionsVersion["version"]

        return request.execute()

    def delete(self, packageName: str, productId: str):
        return (
            self.service.monetization()
            .subscriptions()
            .delete(
                packageName=packageName,
                productId=productId,
            )
        ).execute()


class GooglePlayPurchase:
    def __init__(self, credentials: Credentials):
        self.subscription = GooglePlayPurchaseSubscription(credentials)


class GooglePlayPurchaseSubscription(GooglePlayPublisherService):
    def get(self, packageName: str, token: str) -> TypeSubscriptionPurchase:
        return (
            self.service.purchases()
            .subscriptionsv2()
            .get(
                packageName=packageName,
                token=token,
            )
            .execute()
        )

    def verify(self, packageName: str, token: str):
        subscription = self.get(packageName, token)

        if subscription[
            "acknowledgementState"
        ] == TypeAcknowlegementState.ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED and subscription[
            "subscriptionState"
        ] in (
            TypeSubscriptionState.SUBSCRIPTION_STATE_ACTIVE,
            TypeSubscriptionState.SUBSCRIPTION_STATE_IN_GRACE_PERIOD,
        ):
            return True, subscription

        return False, subscription


googleplay = GooglePlay(
    Credentials.from_service_account_file(BASE_DIR / "payment/credentials.json"),
)
