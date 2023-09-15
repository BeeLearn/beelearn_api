from typing import Any
from django.db import models


def get_revision_mixin(
    creator_related_name=None,
    editor_related_name=None,
):
    from account.models import User

    class RevisionMixin(models.Model):
        creator = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name=creator_related_name,
        )

        editors = models.ManyToManyField(
            User,
            blank=True,
            related_name=editor_related_name,
        )

        @classmethod
        def get_edited(cls, user: User):
            return cls.objects.filter(editors=user)

        @classmethod
        def get_created(cls, user: User):
            return cls.objects.filter(creator=user)

        @classmethod
        def total_edited(cls, user: User):
            return cls.objects.filter(editors=user).count()

        @classmethod
        def total_created(cls, user: User):
            return cls.objects.filter(creator=user).count()

        class Meta:
            abstract = True

    return RevisionMixin


class TimestampMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    pass


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def delete(
        self, using: Any = ..., keep_parents: bool = ...
    ) -> tuple[int, dict[str, int]]:
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True
