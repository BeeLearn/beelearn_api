from typing import List

from django.utils import timezone
from django.dispatch import receiver
from django.db.models import signals

from rest_framework.authtoken.models import Token

from firebase_admin.messaging import subscribe_to_topic, unsubscribe_from_topic

from reward.models import Streak
from .models import Notification, Profile, Settings, User


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


@receiver(signals.post_save, sender=Settings)
def on_user_settings_changed(instance: Settings, update_fields: List[str], **kwargs):
    """
    listen to user settings change
    """
    if instance.fcm_token:
        # subscribe ot unsubscribe user from topics when is_push_notifications_enabled is updated
        if update_fields and "is_push_notifications_enabled" in update_fields:
            if instance.is_push_notifications_enabled:
                for label in Notification.Topic.labels:
                    subscribe_to_topic(instance.fcm_token, label)
            else:
                for label in Notification.Topic.labels:
                    unsubscribe_from_topic(instance.fcm_token, label)
