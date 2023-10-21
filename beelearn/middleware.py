from typing import Any

from django.http import HttpRequest


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        print(request.body)
        response = self.get_response(request)
        if hasattr(response, "data"):
            print(response.data)

        return response
