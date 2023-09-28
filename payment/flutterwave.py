import os
from requests import post
from abc import ABC, abstractproperty
from typing import Optional, TypedDict

from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import APIException, ValidationError

from rave_python import Rave


class HttpException(APIException):
    pass


def _has_required_fields(data: dict, keys: str):
    """
    check if dict has all required keys
    """
    not_found_keys = set(filter(lambda key: not key in data, keys))

    if len(not_found_keys) > 0:
        raise ValidationError(
            {
                "errors": list(
                    map(lambda key: "%s is required" % key, not_found_keys),
                ),
            }
        )


class Flutterwave:
    base_url: str = "https://api.flutterwave.com/"

    def __init__(
        self, secret_key: Optional[str] = None, public_key: Optional[str] = None
    ):
        self.__secret_key = secret_key or os.environ.get("RAVE_SECRET_KEY")
        self.__public_key = public_key or os.environ.get("RAVE_PUBLIC_KEY")
        assert (
            self.__public_key is not None
        ), "set a .env vairable with FLUTTEWAVE_PUBLIC_KEY or provide it explicitly"
        assert (
            self.__secret_key is not None
        ), "set a .env vairable with FLUTTERWAVE_SECRET_KEY or provide it explicitly"

        self.charge = Charge(self)
        self.rave = Rave(self.__public_key)

    @property
    def headers(self):
        return {"Authorization": "Bearer %s" % self.__secret_key}


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


class Api(ABC):
    def __init__(self, flutterwave: Flutterwave):
        self.flutterwave = flutterwave

    @abstractproperty
    @property
    def api_path(self):
        pass

    @property
    def api_url(self) -> str:
        return self.flutterwave.base_url + self.api_path


class Charge(Api):
    @property
    def api_path(self):
        return "v3/payments"

    def standard(self, data: TStandard) -> TStandardResponse:
        """
        generate a payment link using flutterwave standard api
        """
        _has_required_fields(
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
            headers=self.flutterwave.headers,
        )

        if response.status_code == HTTP_200_OK:
            return response.json()
        print(response.status_code)
        raise APIException(
            response.content,
            response.status_code,
        )
