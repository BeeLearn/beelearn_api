from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from rest_framework.permissions import AllowAny

from .models import Tag, Category
from .serializers import TagSerializer, CategorySerializer

class CategoryViewSet(GenericViewSet, ListModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class TagViewSet(GenericViewSet, ListModelMixin):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    