from abc import ABC, abstractproperty
from requests import Response
from rest_framework import status, exceptions


def has_required_fields(data: dict, keys: str):
    """
    check if dict has all required keys
    """
    not_found_keys = set(filter(lambda key: not key in data, keys))

    if len(not_found_keys) > 0:
        raise exceptions.ValidationError(
            {
                "errors": list(
                    map(lambda key: "%s is required" % key, not_found_keys),
                ),
            }
        )


def transform_error_response(response: Response):
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        return exceptions.ValidationError(response.content)

    if response.status_code == status.HTTP_404_NOT_FOUND:
        return exceptions.NotFound(response.content)

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        return exceptions.NotAuthenticated(response.content)

    return exceptions.APIException(response.content, response.status_code)


class APICore(ABC):
    base_url: str
    _secret_key: str
    _public_key: str

    @property
    def headers(self):
        return {
            "Authorization": "Bearer %s" % self._secret_key,
        }


class API(ABC):
    api_path: str

    def __init__(self, core: APICore):
        self.core = core

    @property
    def api_url(self) -> str:
        return self.core.base_url + self.api_path

    def get_detailed_url(self, path: str):
        return (
            self.api_url + path if path.startswith("/") else self.api_url + "/" + path
        )
