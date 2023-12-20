from django.dispatch import receiver
from django.db.models.signals import post_save

from account.models import User

from .legacy_models import generate_user_category_feed

# todo move this to run in background using celery
@receiver(post_save, sender=User)
def generate_user_category_feed_on_user_created(
    instance: User,
    created: bool,
    **kwargs,
):
    if created:
        generate_user_category_feed(instance)
