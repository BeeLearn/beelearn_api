from django.db import models

from beelearn.models import TimestampMixin


class Category(TimestampMixin):
    name = models.CharField(
        max_length=60,
        unique=True,
    )

    icon = models.ImageField(upload_to="assets/tags/icons")

    def __str__(self):
        return self.name


class Tag(TimestampMixin):
    name = models.CharField(
        max_length=60,
        unique=True,
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
