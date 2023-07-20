from django.apps import AppConfig


class RewardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reward"

    def ready(self):
        import reward.signals
