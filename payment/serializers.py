from rest_framework import serializers

from django_restql.fields import NestedField


from .models import Product, Purchase


class ProductSerializer(serializers.ModelSerializer):
    """
    Product model serializer
    """

    class Meta:
        model = Product
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    """
    Purchase model serializer
    """
    from account.serializers import UserSerializer


    user = NestedField(
        UserSerializer,
        write_only=True,
    )
    product = NestedField(ProductSerializer)

    class Meta:
        model = Purchase
        fields = "__all__"
