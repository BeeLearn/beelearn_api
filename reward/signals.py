import random

from typing import List, Set

from django.utils import timezone
from django.dispatch import receiver
from django.db.models import signals

from account.models import Profile, User
from beelearn.utils import get_week_start_and_end
from catalogue.models import Course, Lesson
from messaging.models import Thread
from reward.models import Price, Reward, Streak


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
def award_price_to_user(instance: Reward, pk_set: Set[int], **kwargs):
    """
    Award achievement price to user
    """
    profiles = []
    users = User.objects.filter(pk__in=pk_set)

    for user in users:
        user.profile.xp += instance.price.xp
        user.profile.bits += instance.price.bits

        profiles.append(user.profile)

    Profile.objects.bulk_update(profiles, fields=["xp", "bits"])


@receiver(signals.m2m_changed, sender=Streak.streak_complete_users.through)
def award_streak_price_to_user(pk_set: Set[int], **kwargs):
    """
    Award price to user on complete streak
    """

    prices = Price.objects.filter(type=Price.PriceType.STREAK_COMPLETE)
    users = User.objects.filter(pk__in=pk_set)

    if len(prices) > 0:
        profiles = []
        price = random.choice(prices)

        for user in users:
            user.profile.xp += price.xp
            user.profile.bits += price.bits

            profiles.append(user.profile)

        Profile.objects.bulk_update(profiles, ["xp", "bits"])


@receiver(signals.m2m_changed, sender=Streak.streak_complete_users.through)
def streak_complete(instance: Streak, pk_set: Set[int], action: str, **kwargs):
    # increase streak count on completion
    if action == "post_add":
        if instance.date == timezone.now().date():
            week_start, week_end = get_week_start_and_end(instance.date)

            for user in User.objects.filter(pk__in=pk_set):
                streaks = Streak.objects.filter(
                    date__gte=week_start,
                    date__lte=week_end,
                    streak_complete_users=user,
                )

                if streaks.count() == 7:
                    profile = Profile.objects.get(user=user)
                    profile.streaks = profile.streaks + 1
                    profile.save(update_fields=["streaks"])
