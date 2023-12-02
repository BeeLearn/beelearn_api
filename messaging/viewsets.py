from rest_framework import viewsets, mixins

from .models import Comment, Reply, Thread
from .serializers import CommentSerializer, ReplySerializer, ThreadSerializer


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Comment.objects.prefetch_related(
        "user",
        "likes",
        "replies",
    ).all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        match self.request.method:
            case "GET" | "PATCH":
                return self.queryset
            case "POST" | "DELETE":
                return self.queryset.filter(user=self.request.user)


class ThreadViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    filter_fields = ("reference",)


class ReplyViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Reply.objects.prefetch_related(
        "comment",
        "comment__user",
        "comment__likes",
        "comment__replies",
    ).all()

    filter_fields = (
        "parent",
        "comment",
    )

    serializer_class = ReplySerializer
