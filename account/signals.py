from typing import List

from django.utils import timezone
from django.dispatch import receiver
from django.db.models import signals

from rest_framework.authtoken.models import Token

from reward.models import Streak
from .models import Profile, Settings, User


@receiver(signals.post_save, sender=User)
def create_new_user_token(instance: User, created: bool, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(signals.post_save, sender=User)
def create_new_user_profile_and_settings(instance: User, created: bool, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Settings.objects.create(user=instance)


@receiver(signals.post_save, sender=Profile)
def on_profile_saved(
    instance: Profile, created: bool, update_fields: List[str], **kwargs
):
    if not created:
        if update_fields and "streaks" in update_fields:
            return

        today = timezone.now()
        streak, created = Streak.objects.get_or_create(date=today.date())

        if not created:
            streak.streak_complete_users.remove(instance.user)
            streak.save()
