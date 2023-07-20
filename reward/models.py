from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Price(models.Model):
    """
    Priced rewards, given on completion of certain tasks
    """

    class PriceType(models.TextChoices):
        REWARD_ACHIEVE = "REWARD_ACHIEVE", "Reward achieved"
        LESSON_COMPLETE = "LESSON_COMPLETE", "Lesson completed"
        STREAK_COMPLETE = "STREAK_COMPLETE", "Streak completed"

    type = models.TextField(choices=PriceType.choices)
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
        WHERE_THE_MAGIC_HAPPENS= "WHERE_THE_MAGIC_HAPPENS"
        JUST_GETTING_STARTED = "JUST_GETTING_STARTED"

        # api base rewards
        FEARLESS = "FEARLESS"

        # engagement base rewards
        ENGAGED_IN = "ENGAGED_IN"
        WE_ARE_IN_THIS_TOGETHER = "WE_ARE_IN_THIS_TOGETHER"

    type = models.TextField(choices=RewardType.choices)

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

    def __str__(self):
        return self.title


class Achievement(models.Model):
    """
    User unlocked reward collections
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    reward = models.ForeignKey(
        Reward,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.reward.title


class Streak(models.Model):
    pass
