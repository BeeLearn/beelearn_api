from django.dispatch import receiver
from django.db.models import signals

from rest_framework.authtoken.models import Token

from account.models import User


@receiver(signals.post_save, sender=User)
def create_token_on_new_user(instance: User, created: bool):
    if created:
        Token.objects.create(user=instance)
