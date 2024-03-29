from logging import getLogger
from typing import Any
from django.http import HttpRequest

logger = getLogger(__name__)


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # print(
        #     "%s[%s] request body:"
        #     % (
        #         request.get_full_path(),
        #         request.method,
        #     ),
        #     request.body,
        # )

        response = self.get_response(request)

        # if hasattr(response, "data"):
        #     print(
        #         "%s[%s] response body:"
        #         % (
        #             request.get_full_path(),
        #             response.data,
        #         ),
        #         request.body,
        #     )

        return response


class OverrideRequestDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Any:
        pass 