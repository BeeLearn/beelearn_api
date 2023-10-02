import os
from typing import Generic, List, Literal, TypeVar, TypedDict

from rest_framework import status, exceptions

from requests import get, post

from beelearn.external_api import (
    API,
    APICore,
    has_required_fields,
    transform_error_response,
)


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

class TypeTransactionInitialize(TypedDict):
    plan: str
    currency: str
    metadata: dict
    reference: str
    callback_url: str
    invoice_limit: str
    channels: List[
        Literal[
            "qr",
            "card",
            "bank",
            "ussd",
            "mobile_money",
            "bank_transfer",
            "eft",
        ]
    ]
    split_code: str
    subaccount: str
    transaction_charge: str
    bearer: Literal["account", "subaccount"]


class TypeTransactionData(TypedDict):
    id: int
    fees: int
    domain: str
    status: str
    amount: str
    message: str
    paid_at: str
    channel: str
    reference: str
    created_at: str
    geteway_response: str
    fees_split: str | None


TData = TypeVar("TData")


class TypeResponse(Generic[TData]):
    status: bool
    message: str
    data: TData


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


paystack = Paystack()
