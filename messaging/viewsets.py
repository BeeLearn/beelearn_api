from rest_framework import viewsets, mixins

from .models import Thread
from .serializers import ThreadSerializer


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    filter_fields = ("is_parent",)

    def get_queryset(self):
        match self.request.method:
            case "GET":
                return self.queryset
            case "POST" | "PATCH" | "DELETE":
                return self.queryset.filter(user=self.request.user)


class ReplyViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Thread.objects.filter(
        is_parent=False,
    )

    serializer_class = ThreadSerializer
