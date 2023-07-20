from rest_framework.routers import DefaultRouter

from .viewsets import UserViewSet

account_router = DefaultRouter()

account_router.register(r"users", UserViewSet)
