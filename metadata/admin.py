from django.contrib import admin

from .models import Tag, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "is_verified",
    )

    def is_verified(self, instance: Tag):
        return instance.category is not None
