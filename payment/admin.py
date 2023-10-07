from django.contrib import admin

from .models import Product, Purchase


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "flutterwave_plan_id",
        "paystack_plan_code",
    )

    search_fields = (
        "name",
        "price",
        "flutterwave_plan_id",
        "paystack_plan_code",
    )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "status",
        "web_order_id",
        "order_id",
    )

    search_fields = (
        "user",
        "product",
    )
