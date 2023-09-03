from pathlib import Path

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from martor.models import MartorField

from beelearn.models import TimestampMixin


User = get_user_model()


class Course(TimestampMixin):
    """
    Collection of lessons
    """

    COURSE_IMAGE_PATH = Path("assets/courses")

    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to=COURSE_IMAGE_PATH / "backgrounds")
    description = models.TextField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Course detailed description (Optional)",
    )
    is_visible = models.BooleanField(
        default=True,
    )
    course_enrolled_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="course_enrolled_users",
    )
    course_complete_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="course_complete_users",
    )  # users that have complete this course

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-updated_at", "-created_at")


class Module(TimestampMixin):
    """
    Course module collections
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=60)
    is_visible = models.BooleanField(
        default=True,
    )
    entitled_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="module_entitled_users",
    )
    module_complete_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="complete_users",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-updated_at", "-created_at")


class Lesson(TimestampMixin):
    """
    Module lesson collections
    """

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=60)
    is_visible = models.BooleanField(
        default=True,
    )
    entitled_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="lesson_entitled_users",
    )  # users that have access to this course
    lesson_complete_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="lesson_complete_users",
    )  # user have complete this topic

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-updated_at", "-created_at")


class Topic(TimestampMixin):
    """
    Topic is the root representation of a course content
    """

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=128)
    content = MartorField(
        blank=True,
        null=True,
    )
    is_visible = models.BooleanField(
        default=True,
    )
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name="topic_likes",
    )
    entitled_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="topic_entitled_users",
    )
    topic_complete_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="topic_complete_users",
    )

    question_content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    question_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )
    question = GenericForeignKey(
        "question_content_type",
        "question_id",
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_at", "-updated_at")


class TopicComment(TimestampMixin):
    """
    Topic comments
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
    )
    content = models.TextField()

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ("-updated_at", "created_at")


class Category(TimestampMixin):
    """
    Collections of courses that are related
    """

    courses = models.ManyToManyField(Course, blank=True)
    name = models.TextField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("-updated_at", "created_at")
