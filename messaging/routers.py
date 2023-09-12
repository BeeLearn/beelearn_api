from rest_framework.routers import DefaultRouter

from .viewsets import ReplyViewSet, ThreadViewSet

messaging_router = DefaultRouter()

messaging_router.register("threads", ThreadViewSet)
messaging_router.register("replies", ReplyViewSet)
