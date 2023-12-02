from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from .models import Tag
from .serializers import TagSerializer

class TagViewSet(GenericViewSet, ListModelMixin):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    