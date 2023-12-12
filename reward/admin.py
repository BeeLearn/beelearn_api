from django.contrib import admin

from .models import Price, Reward, Streak


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "xp",
        "bits",
    )


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "description",
    )


@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
    )

    list_filter = ("date",)
