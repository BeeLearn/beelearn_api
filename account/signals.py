
from django.dispatch import receiver
from django.db.models import signals
from django.db.models import Prefetch

from rest_framework.authtoken.models import Token

from beelearn.art import create_avatar
from beelearn.utils import get_update_fields
from reward.constants import (
    REWARD_LEVEL_UP_IMAGE,
    REWARD_LIVE_LEVEL_1_IMAGE,
    REWARD_LIVE_LEVEL_DECREASE_1_IMAGE,
)

from .models import Notification, Profile, Settings, User


@receiver(signals.pre_save, sender=User)
def override_user_fields(instance: User, **kwargs):
    if not instance.avatar:
        fullname = instance.get_full_name()
        instance.avatar = create_avatar(
            (fullname if len(fullname) > 1 else instance.email or instance.username)[:2]
        )


@receiver(signals.post_save, sender=User)
def create_new_user_token(instance: User, created: bool, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(signals.post_save, sender=User)
def create_new_user_profile_and_settings(instance: User, created: bool, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Settings.objects.create(user=instance)


@receiver(signals.pre_save, sender=Profile)
def on_profile_changed(
    instance: Profile,
    **kwargs,
):
    """
    listen to profile fields changed
    when xp changed send notification
    """
    profile = Profile.objects.prefetch_related(
        Prefetch(
            "user",
            User.objects.only("id"),
        )
    ).filter(id=instance.pk).first()

    if profile is None:
        return
    
    update_fields = get_update_fields(
        profile,
        instance,
    )
    # check if user leveled up when user level up
    if "xp" in update_fields:
        # could have use a grt condition but this seem more locked in for error correction
        if instance.level == profile.level + 1:
            Notification.objects.create(
                user=profile.user,
                topic=Notification.Topic.LEVEL,
                title="You've just got to level %d!" % instance.level,
                image=REWARD_LEVEL_UP_IMAGE,
                body="Earn more xp to level-up to level %d. Keep the momentum going."
                % (instance.level + 1),
            )

    if "lives" in update_fields:
        if instance.lives == profile.lives + 1:
            Notification.objects.create(
                user=profile.user,
                topic=Notification.Topic.LIVE,
                image=REWARD_LIVE_LEVEL_1_IMAGE,
                title="An Extra Life Beckons!",
                body="You've just gained an additional life. Stay unstoppable on your learning journey.",
            )

        if instance.lives == profile.lives - 1:
            Notification.objects.create(
                user=profile.user,
                topic=Notification.Topic.LIVE,
                image=REWARD_LIVE_LEVEL_DECREASE_1_IMAGE,
                title="Oh No! A Life Lost.",
                body="Refill your hearts to keep the lessons flowing smoothly. You've got this!",
            )
