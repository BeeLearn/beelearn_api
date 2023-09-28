from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from socketio import AsyncServer


from djira.models import Realtime
from beelearn.asgi import sio

sio: AsyncServer = sio


@action(["POST"])
def flutterwave_webhook(request: Request):
    # todo implement flutterwave webhook handler
    return Response()


def playstore_inapp_purchase_webhook(request: Request):
    """
    Listen to
    """
    realtime = Realtime()

    sio.emit(
        "purchases",
        {},
        to=realtime.sid,
    )
