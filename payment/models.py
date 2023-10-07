from uuid import uuid4
from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator

from account.models import User
from beelearn.models import TimestampMixin


class Product(TimestampMixin):
    """
    Products can be consumable or non-consumable
    """

    id = models.CharField(
        unique=True,
        max_length=32,
        primary_key=True,
    )
    name = models.TextField()
    price = models.TextField()
    amount = models.TextField()
    currency = models.TextField()
    description = models.TextField()
    flutterwave_plan_id = models.TextField(
        blank=True,
        null=True,
    )  # allow null to create flutterwave planId using signals notnull
    paystack_plan_code = models.TextField(
        blank=True,
        null=True,
    )  # allow null to create paystack planCode using signals notnull
    consumable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Purchase(TimestampMixin):
    """
    User purchased products
    """

    class Status(models.TextChoices):
        FAILED = "FAILED", "Failed"
        PENDING = "PENDING", "Pending"
        UNKNOWN = "UNKNOWN", "Unknown"
        CANCELED = "CANCELED", "Canceled"
        SUCCESSFUL = "SUCCESSFUL", "Successful"

    order_id = models.TextField(
        null=True,
        blank=True,
    )

    web_order_id = models.TextField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        User,
        related_name="purchases",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    token = models.TextField(
        null=True,
        blank=True,
    )
    status = models.TextField(
        choices=Status.choices,
        default=Status.UNKNOWN,
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username if self.user else self.token
