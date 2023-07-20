from django.contrib import admin

from .models import Price, Reward, Achievement

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    pass

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    pass

