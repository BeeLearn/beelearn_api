from django.dispatch import receiver
from django.db.models import signals

from rest_framework.authtoken.models import Token

from .models import Profile, User


@receiver(signals.post_save, sender=User)
def create_new_user_token(instance: User, created: bool, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(signals.post_save, sender=User)
def create_new_user_profile(instance: User, created: bool, **kwargs):
    if created:
        Profile.objects.create(user=instance)
