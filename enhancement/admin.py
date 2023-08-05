from django.contrib import admin

from .models import Enhancement


# Register your models here.
@admin.register(Enhancement)
class EnhancementAdmin(admin.ModelAdmin):
    pass
