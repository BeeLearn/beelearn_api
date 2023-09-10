from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from beelearn.models import TimestampMixin


class User(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        CURATOR = "CURATOR", "Curator"
        SPECIALIST = "SPECIALIST", "Specialist"

    uid = models.TextField(default=uuid4, unique=True)
    user_type = models.TextField(
        choices=UserType.choices,
        default=UserType.STUDENT,
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = (
        "uid",
        "email",
    )

    def __str__(self):
        return self.username or self.email or self.uid


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
    streaks = models.IntegerField(default=0)  # total number of completed streaks

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


class Settings(TimestampMixin):
    """
    user settings
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    fcm_token = models.TextField(
        null=True,
        blank=True,
    )
    is_promotional_email_enabled = models.BooleanField(default=True)
    is_push_notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email


class Notification(TimestampMixin):
    """
    user notifications
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    small_image = models.ImageField(
        blank=True,
        null=True,
    )
    content = models.TextField()
    intent_to = models.TextField(
        null=True,
        blank=True,
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
