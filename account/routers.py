from rest_framework.routers import DefaultRouter

from .viewsets import UserCourseViewSet

account_router = DefaultRouter()

account_router.register(r"courses", UserCourseViewSet)
