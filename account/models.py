from uuid import uuid4

from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from beelearn.models import TimestampMixin
from beelearn.utils import truncate_string

from metadata.models import Category


class User(AbstractUser):
    """
    Override django default user class
    """

    USER_AVATAR_PATH = "assets/users/avatars/"

    profile: "Profile"
    settings: "Settings"
    notifications: QuerySet["Notification"]

    class Gender(models.TextChoices):
        OTHER = "OTHER", "Other"
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    class UserType(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        CURATOR = "CURATOR", "Curator"
        SPECIALIST = "SPECIALIST", "Specialist"

    uid = models.TextField(
        default=uuid4,
        unique=True,
    )
    user_type = models.TextField(
        choices=UserType.choices,
        default=UserType.STUDENT,
    )
    avatar = models.FileField(
        blank=True,
        null=True,
        upload_to=USER_AVATAR_PATH,
    )

    gender = models.TextField(choices=Gender.choices)

    categories = models.ManyToManyField(
        Category,
        blank=True,
    )

    REQUIRED_FIELDS = (
        "password",
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

    daily_streak_minutes = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(240),
        ],
        default=5,
    )  # daily reach read goal to receive streak

    @property
    def level(self):
        return self.xp // 512

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

    class Meta:
        verbose_name_plural = "Settings"


class Notification(TimestampMixin):
    """
    user notifications
    """

    class Topic(models.TextChoices):
        ADS = "ADS", "Ads"
        LIVE = "LIVE", "Live"
        LEVEL = "LEVEL", "Level"
        REWARD = "REWARD", "Reward"
        STREAK = "STREAK", "Streak"
        COMMENT = "COMMENT", "Comment"
        GENERAL = "GENERAL", "General"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    icon = models.URLField(
        blank=True,
        null=True,
    )
    image = models.URLField()
    title = models.TextField()
    body = models.TextField()
    topic = models.TextField(choices=Topic.choices)
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return truncate_string(self.body)

    class Meta:
        ordering = ("-created_at", "-updated_at")
