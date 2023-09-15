from django.contrib import admin

from .models import Comment, Reply, Thread


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "content",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user",
        "content",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "comment",
    )

    search_fields = ("reference",)


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = (
        "parent",
        "comment",
    )

    search_fields = ("parent",)
