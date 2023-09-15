from rest_framework.routers import DefaultRouter

from .viewsets import CommentViewSet, ReplyViewSet, ThreadViewSet

messaging_router = DefaultRouter()

messaging_router.register("comments", CommentViewSet)
messaging_router.register("threads", ThreadViewSet)
messaging_router.register("replies", ReplyViewSet)
