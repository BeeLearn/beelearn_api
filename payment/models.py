from django.db import models
from django.core.validators import MinValueValidator

from account.models import User
from beelearn.models import TimestampMixin


class Product(TimestampMixin):
    """
    Products can be consumable or non-consumable
    """

    class Period(models.TextChoices):
        YEARLY = "YEARLY", "Yearly"
        MONTHLY = "MONTHLY", "Monthly"
        LIFETIME = "LIFETIME", "LifeTime"
        QUARTERLY = "QUARTERLY", "Quarterly"

    skid = models.CharField(
        null=True,
        blank=True,
        max_length=32,
    )
    name = models.CharField(max_length=128)
    price = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ],
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    period = models.TextField(choices=Period.choices)
    flutterwave_plan_id = models.TextField(
        blank=True,
        null=True,
    )
    is_premium = (
        models.BooleanField()
    )  # determines if user purchase this products the they are premium users

    def __str__(self):
        return self.name


class Purchase(TimestampMixin):
    """
    User purchased products
    """

    class Status(models.TextChoices):
        FAILED = "FAILED", "FAILED"
        PENDING = "PENDING", "PENDING"
        SUCCESSFUL = "SUCCESSFUL", "SUCCESSFUL"

    user = models.ForeignKey(
        User,
        related_name="purchases",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    reference = models.TextField(
        null=True,
        blank=True,
    )
    status = models.TextField(
        choices=Status.choices,
        default=Status.PENDING,
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username
