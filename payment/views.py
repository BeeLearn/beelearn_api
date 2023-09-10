from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


@action(["POST"])
def flutterwave_webhook(request: Request):
    # todo implement flutterwave webhook handler
    return Response()
