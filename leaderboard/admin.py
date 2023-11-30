from django.contrib import admin

from .models import League, UserLeague


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
    )


@admin.register(UserLeague)
class UserLeagueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "league",
        "xp",
        "xp_before",
    )
