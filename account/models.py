from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    uid = models.TextField(default=uuid4)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    is_email_verified = models.BooleanField(default=False)
    lives = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        default=3,
    )
    xp = models.IntegerField(default=0)  # experience point
    bits = models.IntegerField(default=0)  # used to unlock questions

    daily_streak_minutes = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(240),
        ],
        default=5,
    )  # daily reach read goal to receive streak

    @property
    def level(self):
        return self.xp // 1024

    def __str__(self):
        return self.user.email
