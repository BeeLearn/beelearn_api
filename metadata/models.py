from django.db import models

from beelearn.models import TimestampMixin


class Tag(TimestampMixin):
    name = models.CharField(
        max_length=60,
        unique=True,
    )

    def __str__(self):
        return self.name

