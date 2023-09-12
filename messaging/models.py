import re
from typing import List

from django.db import models

from beelearn.models import TimestampMixin
from account.models import User


class Comment(TimestampMixin):
    MENTION_REGEX = r"(^|[^@\w])@(\w{3,16})"

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )
    content = models.TextField()
    is_parent = models.BooleanField()
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name="thread_likes",
    )

    @property
    def mentions(self):
        mentions: List[str] = [
            mention
            for _, mention in re.findall(
                self.MENTION_REGEX,
                self.content,
            )
        ]

        return User.objects.filter(username__in=mentions).exclude(id=self.user.pk)

    class Meta:
        abstract = True


class Thread(Comment):
    replies = models.ManyToManyField(
        "self",
        blank=True,
        through="Reply",
        through_fields=("parent", "comment"),
    )


class Reply(TimestampMixin):
    comment = models.OneToOneField(
        Thread,
        on_delete=models.CASCADE,
        related_name="reply_comment",
    )
    parent = models.ForeignKey(
        Thread,
        null=True,
        on_delete=models.CASCADE,
        related_name="reply_parent",
    )

    class Meta:
        verbose_name_plural = "replies"