from django.core.cache import cache

from rest_framework import serializers

from django_restql.fields import NestedField
from django_restql.serializers import NestedModelSerializer

from .googleplay import googleplay


from .models import Product, Purchase


class ProductSerializer(NestedModelSerializer):
    """
    Product model serializer
    """
    class Meta:
        model = Product
        fields = "__all__"


class PurchaseSerializer(NestedModelSerializer):
    """
    Purchase model serializer
    """

    from account.serializers import UserSerializer

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    product = NestedField(ProductSerializer)

    class Meta:
        model = Purchase
        fields = "__all__"
