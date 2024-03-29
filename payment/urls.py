from django.urls import path
from payment.views import flutterwave_webhook, googleplay_store_webhook, paystack_webhook


urlpatterns = [
    path(r"flutterwave/", flutterwave_webhook),
    path(r"paystack/", paystack_webhook),
    path(r"googleplay/", googleplay_store_webhook),
]
