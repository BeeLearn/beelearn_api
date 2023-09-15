import re, uuid
from typing import List

from django.db import models

from beelearn.models import SoftDeleteMixin, TimestampMixin
from account.models import User


class Comment(SoftDeleteMixin, TimestampMixin):
    """
    super comment with sub replies
    """

    MENTION_REGEX = r"(^|[^@\w])@(\w{3,16})"

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )
    content = models.TextField()
    replies = models.ManyToManyField(
        "self",
        blank=True,
        through="Reply",
        through_fields=("parent", "comment"),
    )
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

        print(mentions)

        return User.objects.filter(username__in=mentions).exclude(id=self.user.pk)

    def __str__(self):
        return "@%s %s" % (self.user.username, self.content[:16])


class Reply(TimestampMixin):
    """
    Reply to comments
    """

    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
        related_name="reply_comment",
    )
    parent = models.ForeignKey(
        Comment,
        null=True,
        on_delete=models.CASCADE,
        related_name="reply_parent",
    )

    def __str__(self):
        return str(self.comment)

    class Meta:
        verbose_name_plural = "replies"


class Thread(TimestampMixin):
    """
    Thread is micro messaging inform of comments.
    This should be an abtract but to make realtime code reusable we have set reference from thread owner
    ```
    class Topic:
        thread_reference = models.UUIDField(default=uuid.uuid4)
        ...

    top_level_comments = Thread.objects.filter(reference=topic.thread_reference)
    ```
    """

    reference = models.UUIDField()
    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.reference)
