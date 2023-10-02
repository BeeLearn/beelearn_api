from typing import Literal
from rest_framework import status, exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .paystack import paystack
from .flutterwave import Flutterwave
from .models import Product, Purchase
from .inapp_purchase import InAppPurchase
from .serializers import InAppPurchaseSerializer, ProductSerializer, PurchaseSerializer

flutterwave = Flutterwave()


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseViewSet(ModelViewSet):
    lookup_value_regex = r"[A-Za-z0-9.-]+"
    queryset = Purchase.objects.prefetch_related("product")
    serializer_class = PurchaseSerializer

    @action(methods=["POST"], detail=False)
    def verify(self, request: Request):
        serializer = InAppPurchaseSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        purchase, _ = InAppPurchase.verify(request.user, data)

        return Response(
            self.get_serializer(purchase).data, status=status.HTTP_201_CREATED
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path="create-payment-link",
    )
    def create_payment_link(self, request: Request):
        """
        create flutterwave payment link for client
        """
        data = request.data
        source: Literal["paystack", "flutterwave"] = data.get("source", "paystack")

        if source == "paystack":
            response = paystack.transaction.initialize(data)
        elif source == "flutterwave":
            response = flutterwave.charge.standard(data)
        else:
            raise exceptions.ValidationError(
                {"errors": ["source %s is not supported" % source]}
            )
        return Response(
            data={
                "source": source,
                "data": response["data"],
            },
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
