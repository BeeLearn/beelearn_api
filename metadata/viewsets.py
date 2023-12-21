from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin


from .models import Tag, Category
from .serializers import TagSerializer, CategorySerializer


class CategoryViewSet(GenericViewSet, ListModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(tags__courses__isnull=False)

    search_fields = ("name",)

class TagViewSet(GenericViewSet, ListModelMixin):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    search_fields = (
        "name",
        "category__name",
    )
