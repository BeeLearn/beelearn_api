from django.urls import path, include

from catalogue.routers import catalogue_router
from account.routers import account_router

urlpatterns = [
    path(r"catalogue/", include(catalogue_router.urls)),
    path(r"account/", include(account_router.urls)),
]
