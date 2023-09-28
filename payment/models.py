from django.db import models
from django.core.validators import MinValueValidator

from account.models import User
from beelearn.models import TimestampMixin


class Product(TimestampMixin):
    """
    Products can be consumable or non-consumable
    """
    sku_id = models.CharField(max_length=32)
    price = models.TextField()
    amount = models.TextField()
    currency = models.TextField()
    name = models.TextField()
    description = models.TextField()
    flutterwave_plan_id = models.TextField(
        blank=True,
        null=True,
    ) # allow null to create flutterwave planId using signals notnull
    consumable = models.BooleanField(default=False)
    def __str__(self):
        return self.sku_id
 

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
    ) # same as purchase token
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
