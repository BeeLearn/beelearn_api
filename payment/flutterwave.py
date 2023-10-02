import os
from requests import post
from typing import Optional, TypedDict

from rest_framework.status import HTTP_200_OK

from rave_python import Rave

from beelearn.external_api import (
    API,
    APICore,
    has_required_fields,
    transform_error_response,
)


class Flutterwave(APICore):
    base_url = "https://api.flutterwave.com/"

    def __init__(
        self, secret_key: Optional[str] = None, public_key: Optional[str] = None
    ):
        self._secret_key = secret_key or os.environ.get("RAVE_SECRET_KEY")
        self._public_key = public_key or os.environ.get("RAVE_PUBLIC_KEY")
        assert (
            self._public_key is not None
        ), "set a .env vairable with FLUTTEWAVE_PUBLIC_KEY or provide it explicitly"
        assert (
            self._secret_key is not None
        ), "set a .env vairable with FLUTTERWAVE_SECRET_KEY or provide it explicitly"

        self.charge = Charge(self)
        self.rave = Rave(self._public_key)


class TFlutterwaveResponse(TypedDict):
    status: str
    message: str
    data: any


class TStandard(TypedDict):
    tx_ref: str
    amount: str
    currency: str
    customer: str
    redirect_url: str
    meta: Optional[dict]
    customization: Optional[dict]


class TStandardResponseData(TypedDict):
    link: str


class TStandardResponse(TypedDict):
    data: TStandardResponseData


class Charge(API):
    api_path = "v3/payments"

    def standard(self, data: TStandard) -> TStandardResponse:
        """
        generate a payment link using flutterwave standard api
        """
        has_required_fields(
            data,
            [
                "tx_ref",
                "amount",
                "currency",
                "redirect_url",
                "customer",
            ],
        )

        response = post(
            self.api_url,
            json=data,
            headers=self.core.headers,
        )

        if response.status_code == HTTP_200_OK:
            return response.json()

        raise transform_error_response(response)
