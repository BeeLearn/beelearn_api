from django.contrib import admin

from .models import Product, Purchase


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "period",
        "is_premium",
        "flutterwave_plan_id",
    )

    search_fields = (
        "name",
        "price",
        "flutterwave_plan_id",
    )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "status",
    )

    search_fields = (
        "user",
        "product",
    )
