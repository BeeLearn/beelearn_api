from rest_framework import viewsets, mixins

from .models import Enhancement
from .serializers import EnhancementSerializer


class EnhancementViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Enhancement.objects.all()
    serializer_class = EnhancementSerializer

    filter_fields = ("topic",)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
