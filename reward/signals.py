import random

from typing import List, Set

from django.dispatch import receiver
from django.db.models import signals

from account.models import Notification, Profile, User

from catalogue.models import Course, Lesson
from leaderboard.models import UserLeague

from messaging.models import Thread

from .models import Price, Reward, Streak
from .constants import REWARD_STREAK_IMAGE, REWARD_XP_LEVEL_2_IMAGE


# api
# @receiver(signals.post_save)
# def grant_fearless_reward(instance, **kwargs):
#     """
#     Retry a solution to a question multiple times.
#     """


# @receiver(signals.m2m_changed, sender=Course.course_complete_users.through)
# def grant_new_career_awaits_reward(instance: Course, **kwargs):
#     """
#     Triggered when a user completes all possible courses on a particular topic (rare).
#     """


# @receiver(signals.pre_save)
# def grand_where_the_magic_happens_reward(instance, **kwargs):
#     """
#     Triggered when a user completes a random task (rare).
#     """


# solution
# @receiver(signals.post_save, sender=Achievement)
# def grand_achiever_reward(instance, **kwargs):
#     """
#     Reward a user who has earned more than half of all possible rewards.
#     """


@receiver(signals.post_save, sender=Profile)
def grant_verify_account_reward(instance: Profile, update_fields: List[str], **kwargs):
    """
    Triggered when a user has successfully verified their account.
    """
    if update_fields:
        if "is_email_verified" in update_fields:
            reward = Reward.objects.get(type=Reward.RewardType.VERIFY_ACCOUNT)
            reward.reward_unlocked_users.add(instance.user)


@receiver(signals.post_save, sender=Thread)
def grant_we_are_in_this_together_and_engaged_in_reward(
    instance: Thread, created: bool, **kwargs
):
    """
    Triggered when a user engages in multiple discussions frequently.
    """

    if created:
        user_comment_count = Thread.objects.filter(reference=instance.reference).count()

        # Triggered when a user comments on a lesson.
        if user_comment_count == 1:
            reward = Reward.objects.get(type=Reward.RewardType.WE_ARE_IN_THIS_TOGETHER)
            reward.reward_unlocked_users.add(instance.comment.user)

        if user_comment_count % 10 == 0:
            reward = Reward.objects.get(type=Reward.RewardType.ENGAGED_IN)
            reward.reward_unlocked_users.add(instance.comment.user)


@receiver(signals.m2m_changed, sender=Lesson.lesson_complete_users.through)
def just_getting_started(instance: Lesson, pk_set: Set[int], **kwargs):
    """
    Triggered when a user completes the first lesson in a course.
    """
    
    first_lesson = Lesson.objects.first()  # lessons are order by created_at by default

    if first_lesson == instance:
        reward = Reward.objects.get(type=Reward.RewardType.JUST_GETTING_STARTED)
        users = User.objects.filter(pk__in=pk_set)
        reward.reward_unlocked_users.add(*users)


@receiver(signals.m2m_changed, sender=Course.course_complete_users.through)
def grant_course_master_hat_trick_and_course_ninja_reward(pk_set: Set[int], **kwargs):
    """
    Reward a user for completing courses.
    """

    users = User.objects.filter(pk__in=pk_set)

    # Reward a user who completes a course.
    reward = Reward.objects.get(type=Reward.RewardType.COURSE_MASTER)
    reward.reward_unlocked_users.add(*users)

    for user in users:
        total_user_complete_course = Course.objects.filter(
            course_complete_users__pk=user.pk
        ).count()

        # Reward a user for completing three courses.
        if total_user_complete_course == 3:
            reward = Reward.objects.get(type=Reward.RewardType.HAT_TRICK)
            reward.reward_unlocked_users.add(user)

        # Reward a user for completing ten courses.
        if total_user_complete_course == 10:
            reward = Reward.objects.get(type=Reward.RewardType.COURSE_NINJA)
            reward.reward_unlocked_users.add(user)


@receiver(signals.m2m_changed, sender=Reward.reward_unlocked_users.through)
def award_reward_price_to_user(instance: Reward, pk_set: Set[int], action: str, **kwargs):
    """
    Award achievement price to user
    """
    if action == "post_added":
        profiles = []
        notifications = []
        userleagues = []

        users = User.objects.select_related(
            "profile",
            "settings",
        ).filter(pk__in=pk_set)

        for user in users:
            user.profile.xp += instance.price.xp
            user.profile.bits += instance.price.bits
            # user.userleague.xp += instance.price.xp

            profiles.append(user.profile)
            # userleagues.append(user.userleague)

            notifications.append(
                Notification(
                    user=user,
                    body=instance.description,
                    image=instance.icon.url,
                    topic=Notification.Topic.REWARD,
                    title="%s has been unlocked" % instance.title,
                ),
            )

        Profile.objects.bulk_update(
            profiles,
            fields=["xp", "bits"],
        )
        UserLeague.objects.bulk_update(
            userleagues,
            fields=["xp"],
        )
        Notification.objects.bulk_create(notifications)


@receiver(signals.m2m_changed, sender=Streak.streak_complete_users.through)
def award_streak_price_to_user(pk_set: Set[int], action: str, **kwargs):
    """
    Award price to user on complete streak
    """
    if action == "post_add":
        users = User.objects.filter(pk__in=pk_set)
        prices = Price.objects.filter(type=Price.PriceType.STREAK_COMPLETE)

        if prices.count() == 0:
            return

        profiles = []
        userleagues = []
        notifications = []

        price = random.choice(prices)

        for user in users:
            user.profile.xp += price.xp
            user.profile.bits += price.bits
            # user.userleague.xp += price.xp

            profiles.append(user.profile)
            # userleagues.append(user.userleague)
            notifications.append(
                Notification(
                    user=user,
                    title="Daily Streak Achieved!",
                    body="You've reached your daily goal. Keep collecting those streaks to unlock fantastic rewards.",
                    image=REWARD_STREAK_IMAGE,
                    topic=Notification.Topic.STREAK,
                )
            )

            notifications.append(
                Notification(
                    user=user,
                    title="Daily Streak Reward Unlocked!",
                    body="You've reached your daily goal and unlocked a streak reward!",
                    image=REWARD_XP_LEVEL_2_IMAGE,
                    topic=Notification.Topic.STREAK,
                )
            )

        Profile.objects.bulk_update(
            profiles,
            ["xp", "bits"],
        )
        UserLeague.objects.bulk_update(
            userleagues,
            fields=["xp"],
        )
        Notification.objects.bulk_create(notifications)

        # manually send post_save to notification signals
        for notification in notifications:
            signals.post_save.send(
                Notification,
                instance=notification,
                created=True,
            )
