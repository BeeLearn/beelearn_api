from rest_framework import serializers

from django_restql.fields import NestedField
from django_restql.serializers import NestedModelSerializer


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
    product = NestedField(
        ProductSerializer,
        accept_pk=True,
    )

    class Meta:
        model = Purchase
        fields = "__all__"
        extra_kwargs = {
            "status": {
                "read_only": True,
            },
        }


class InAppPurchaseProductSerializer(serializers.Serializer):
    """
    InAppPurchase Product serializer
    """

    productId = serializers.CharField()
    purchaseId = serializers.CharField()
    androidPackageId = serializers.CharField(default="com.oasis.beelearn")


class InAppPurchaseSerializer(serializers.Serializer):
    """
    InAppPurchase serializer
    """

    token = serializers.CharField()
    product = InAppPurchaseProductSerializer()
    type = serializers.ChoiceField(choices=["consumable", "nonconsumable"])
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    source = serializers.ChoiceField(choices=["google_play", "apple_store"])
