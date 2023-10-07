import os

from rest_framework import status, exceptions

from requests import get, post

from beelearn.external_api import (
    API,
    APICore,
    has_required_fields,
    transform_error_response,
)
from payment.paystack_type import TypeResponse, TypeTransactionData, TypeTransactionInitialize


class Paystack(APICore):
    base_url = "https://api.paystack.co/"

    def __init__(self, public_key: str = None, secret_key: str = None):
        if public_key is None:
            self._public_key = os.environ.get("PAYSTACK_PUBLIC_KEY")

        if secret_key is None:
            self._secret_key = os.environ.get("PAYSTACK_SECRET_KEY")

        assert (
            self._public_key is not None or self._secret_key is not None
        ), "public_key or secret_key can't be None try setting a .env variable named PAYSTACK_PUBLIC_KEY and PAYSTACK_SECRET_KEY"

        self.transaction = PaystackTransaction(self)




class PaystackTransaction(API):
    api_path = "transaction/initialize"

    def initialize(self, data: TypeTransactionInitialize):
        has_required_fields(
            data,
            ["email", "amount"],
        )
        response = post(
            self.api_url,
            json=data,
            headers=self.core.headers,
        )

        if response.status_code == status.HTTP_200_OK:
            return response.json()

        raise exceptions.APIException(
            response.content,
            response.status_code,
        )

    def verify(self, reference: str) -> TypeResponse[TypeTransactionData]:
        response = get(
            self.get_detailed_url(reference),
            headers=self.core.headers,
        )

        if response.status_code == status.HTTP_200_OK:
            return response.json()

        raise transform_error_response(response)


class PaystackSubscription(API):
    api_path = "subscription"

    def get(self, plan_id_or_code: str):
        response = get(
            self.get_detailed_url(plan_id_or_code),
            headers=self.core.headers,
        )

        if response.status_code == status.HTTP_200_OK:
            return response.json()

        raise transform_error_response(response)

    def enable(self, code, token):
        response = post(
            self.get_detailed_url("enable"),
            headers=self.core.headers,
            json={
                "code": code,
                "token": token,
            },
        )

        if response.status_code == status.HTTP_201_CREATED:
            return response.json()

        raise transform_error_response(response)

    def disable(self, code, token):
        response = post(
            self.get_detailed_url("disable"),
            headers=self.core.headers,
            json={
                "code": code,
                "token": token,
            },
        )

        if response.status_code == status.HTTP_201_CREATED:
            return response.json()

        raise transform_error_response(response)

    def update_subscription(self, code):
        response = get(
            self.get_detailed_url("%s/manage/link" % code),
            headers=self.core.headers,
        )

        if response.status_code == status.HTTP_200_OK:
            return response.json()

        raise transform_error_response(response)

    def send_update_subscription_link(self, code):
        response = post(
            self.get_detailed_url("%s/manage/email" % code),
            headers=self.core.headers,
        )

        if response.status_code == status.HTTP_200_OK:
            return response.json()

        raise transform_error_response(response)


paystack = Paystack()
