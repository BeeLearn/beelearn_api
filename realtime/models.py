from django.db import models

from account.models import User


class Realtime(models.Model):
    """
    User realtime connection database cache instance
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    is_online = models.BooleanField(
        default=False,
    )
    sid = models.UUIDField(
        null=True,
        blank=False,
    )

    def __str__(self):
        return self.user.email
