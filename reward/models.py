from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Reward(models.Model):
    """
    Rewards are given to user on completion of certain tasks
    """

    class RewardType(models.TextChoices):
        FEARLESS = "FEARLESS"
        ENGAGED_IN = "ENGAGED_IN"
        GOOD_COMPANY = "GOOD_COMPANY"
        WALK_THE_WALK = "WALK_THE_WALK"
        VERIFY_ACCOUNT = "VERIFY_ACCOUNT"
        PROMISING_PLAYER = "PROMISING_PLAYER"
        NEW_CAREER_AWAITS = "NEW_CAREER_AWAITS"
        WHERE_MAGIC_HAPPEN = "WHERE_MAGIC_HAPPEN"
        JUST_GETTING_STARTED = "JUST_GETTING_STARTED"
        WE_ARE_IN_THIS_TOGETHER = "WE_ARE_IN_THIS_TOGETHER"

        # solution
        ACHIEVER = "ACHIEVER"
        HAT_TRICK = "HAT_TRICK"
        COURSE_MASTER = "COURSE_MASTER"
        SOLUTION_GURU = "SOLUTION_GURU"
        SOLUTION_MASTER = "SOLUTION_MASTER"
        SOLUTION_NINJA = "SOLUTION_NINJA"

    type = models.TextField(choices=RewardType.choices)

    # metadata
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=128)
    icon = models.ImageField(upload_to="assets/rewards/icons")

    # theming
    color = models.CharField(max_length=8)
    dark_color = models.CharField(max_length=8)

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
