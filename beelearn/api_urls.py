from django.urls import path, include

from catalogue.routers import catalogue_router
from account.routers import account_router
from reward.routers import reward_router
from payment.routers import payment_router
from messaging.routers import messaging_router
from enhancement.routers import enhancement_router
from assessment.routers import assessment_router

urlpatterns = [
    path(r"catalogue/", include(catalogue_router.urls)),
    path(r"account/", include(account_router.urls)),
    path(r"reward/", include(reward_router.urls)),
    path(r"payment/", include(payment_router.urls)),
    path(r"messaging/", include(messaging_router.urls)),
    path(r"assessment/", include(assessment_router.urls)),
    path(r"enhancement/", include(enhancement_router.urls)),
]
