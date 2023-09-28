from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .flutterwave import Flutterwave
from .models import Product, Purchase
from .serializers import ProductSerializer, PurchaseSerializer

flutterwave = Flutterwave()


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.prefetch_related("product")
    serializer_class = PurchaseSerializer

    @action(methods=["POST"], detail=False, url_path="create-payment-link")
    def create_payment_link(self, request: Request):
        """
        create flutterwave payment link for client
        """
        response = flutterwave.charge.standard(request.data)

        return Response(data=response["data"])

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
