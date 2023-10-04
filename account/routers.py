from rest_framework.routers import DefaultRouter

from .viewsets import NotificationViewSet, UserViewSet, ProfileSerializer

account_router = DefaultRouter()

account_router.register(r"users", UserViewSet)
account_router.register(r"profiles", ProfileSerializer)
account_router.register("notifications", NotificationViewSet)
