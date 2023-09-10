from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Product, Purchase
from .serializers import ProductSerializer, PurchaseSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.prefetch_related("product")
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
