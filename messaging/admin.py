from django.contrib import admin

from .models import Reply, Thread


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_parent",
        "content",
        "created_at",
        "updated_at",
    )


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass
