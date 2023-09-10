from django.dispatch import receiver
from django.db.models import signals

from .models import Product


@receiver(signals.post_save, sender=Product)
def on_subscription_created(instance: Product, created: bool, **kwargs):
    pass
