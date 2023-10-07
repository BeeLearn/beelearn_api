from django.contrib import admin

from .models import Notification, Settings, User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "user_type",
        "is_staff",
        "is_superuser",
    )

    list_filter = (
        "user_type",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "is_email_verified",
        "lives",
        "xp",
        "bits",
        "daily_streak_minutes",
    )

    list_filter = ("is_email_verified",)

    search_fields = ("user",)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "is_promotional_email_enabled",
        "is_push_notifications_enabled",
    )

    list_filter = (
        "is_promotional_email_enabled",
        "is_push_notifications_enabled",
    )

    search_fields = ("user",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "topic",
        "is_read",
    )
