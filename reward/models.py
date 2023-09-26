from django.db import models
from django.utils.timezone import timedelta, datetime
from django.contrib.humanize.templatetags.humanize import naturalday
from account.models import User

from beelearn.utils import get_week_start_and_end


class Price(models.Model):
    """
    Priced rewards, given on completion of certain tasks
    """

    class PriceType(models.TextChoices):
        REWARD_ACHIEVE = "REWARD_ACHIEVE", "Reward achieved"
        LESSON_COMPLETE = "LESSON_COMPLETE", "Lesson completed"
        STREAK_COMPLETE = "STREAK_COMPLETE", "Streak completed"

    type = models.TextField(
        choices=PriceType.choices,
        max_length=128,
    )
    xp = models.IntegerField()
    bits = models.IntegerField()

    def __str__(self):
        return self.type

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "xp", "bits"],
                name="Price must be unique",
                violation_error_message="Price already exist",
            )
        ]


class Reward(models.Model):
    """
    Rewards are given to user on completion of certain tasks
    """

    class RewardType(models.TextChoices):
        ACHIEVER = "ACHIEVER"
        HAT_TRICK = "HAT_TRICK"
        COURSE_MASTER = "COURSE_MASTER"
        COURSE_NINJA = "COURSE_NINJA"
        VERIFY_ACCOUNT = "VERIFY_ACCOUNT"
        NEW_CAREER_AWAITS = "NEW_CAREER_AWAITS"
        WHERE_THE_MAGIC_HAPPENS = "WHERE_THE_MAGIC_HAPPENS"
        JUST_GETTING_STARTED = "JUST_GETTING_STARTED"

        # api base rewards
        FEARLESS = "FEARLESS"

        # engagement base rewards
        ENGAGED_IN = "ENGAGED_IN"
        WE_ARE_IN_THIS_TOGETHER = "WE_ARE_IN_THIS_TOGETHER"

    type = models.TextField(
        choices=RewardType.choices,
        unique=True,
        max_length=128,
    )

    # metadata
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=128)
    icon = models.ImageField(upload_to="assets/rewards/icons")

    # theming
    color = models.CharField(max_length=11)
    dark_color = models.CharField(max_length=11)

    # price gain
    price = models.ForeignKey(
        Price,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    reward_unlocked_users = models.ManyToManyField(
        User,
        blank=True,
    )

    def __str__(self):
        return self.title


class Streak(models.Model):
    """
    User streak tracker to sync to multiple devices
    """

    date = models.DateField(unique=True)
    streak_complete_users = models.ManyToManyField(
        User,
        blank=True,
    )

    @classmethod
    def create_streak_for_week(cls, start_date: datetime = None):
        """
        create streak for week
        """
        start_date, end_date = get_week_start_and_end(start_date)

        if cls.objects.filter(date=start_date).exists():
            return

        current_date = start_date
        streaks = []

        while current_date <= end_date:
            streaks.append(cls(date=current_date))

            current_date += timedelta(days=1)

        return cls.objects.bulk_create(
            streaks,
            ignore_conflicts=True,
        )

    def __str__(self):
        return naturalday(self.date)
