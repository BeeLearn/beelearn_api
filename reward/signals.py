import random

from typing import List, Set

from django.dispatch import receiver
from django.db.models import signals

from account.models import Profile, User
from catalogue.models import Course, Lesson, TopicComment
from reward.models import Achievement, Price, Reward, Streak

# todo make use of socket to make realtime with frontend


# api
@receiver(signals.post_save)
def grant_fearless_reward(instance, **kwargs):
    """
    Retry a solution to a question multiple times.
    """


@receiver(signals.m2m_changed, sender=Course.course_complete_users.through)
def grant_new_career_awaits_reward(instance: Course, **kwargs):
    """
    Triggered when a user completes all possible courses on a particular topic (rare).
    """


@receiver(signals.pre_save)
def grand_where_the_magic_happens_reward(instance, **kwargs):
    """
    Triggered when a user completes a random task (rare).
    """


# solution
@receiver(signals.post_save, sender=Achievement)
def grand_achiever_reward(instance, **kwargs):
    """
    Reward a user who has earned more than half of all possible rewards.
    """


@receiver(signals.post_save, sender=Profile)
def grant_verify_account_reward(instance: Profile, update_fields: List[str], **kwargs):
    """
    Triggered when a user has successfully verified their account.
    """
    if update_fields:
        if "is_email_verified" in update_fields:
            reward = Reward.objects.get(type=Reward.RewardType.VERIFY_ACCOUNT)
            reward.reward_unlocked_users.add(instance.user)


@receiver(signals.post_save, sender=TopicComment)
def grant_we_are_in_this_together_and_engaged_in_reward(
    instance: TopicComment, created: bool, **kwargs
):
    """
    Triggered when a user engages in multiple discussions frequently.
    """

    if created:
        user_comment_count = TopicComment.objects.filter(
            topic__lesson__module__course=instance.topic.lesson.module.course
        ).count()

        # Triggered when a user comments on a lesson.
        if user_comment_count == 1:
            reward = Reward.objects.get(type=Reward.RewardType.WE_ARE_IN_THIS_TOGETHER)
            reward.reward_unlocked_users.add(instance.user)

        if user_comment_count % 10 == 0:
            reward = Reward.objects.get(type=Reward.RewardType.ENGAGED_IN)
            reward.reward_unlocked_users.add(instance.user)


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
def award_price_to_user(instance: Reward, pk_sets: Set[int], **kwargs):
    """
    Award achievement price to user
    """
    users = User.objects.filter(pk__in=pk_sets)

    for user in users:
        instance.user.profile.xp += instance.reward.price.xp
        instance.user.profile.bits += instance.reward.price.bits

    User.objects.bulk_update(user, fields=["xp", "bits"])


@receiver(signals.post_save, sender=Streak)
def award_streak_price_to_user(instance: Streak, **kwargs):
    """
    Award price to user on complete streak
    """

    if instance.is_complete:
        prices = Price.objects.filter(
            type=Price.PriceType.STREAK_COMPLETE,
        )

        if len(prices) > 0:
            price = random.choice(prices)
            instance.user.profile.xp += price.xp
            instance.user.profile.bits += price.bits
