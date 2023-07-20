from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


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

    @property
    def level(self):
        return self.xp // 1024

    def __str__(self):
        return self.user.email
