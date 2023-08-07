from pathlib import Path

from django.db import models
from django.contrib.auth import get_user_model

from beelearn.models import TimestampMixin


User = get_user_model()


# keep track of course progress using firebase
# firebase support offline cache of failed request when network is unavailable
class Course(TimestampMixin):
    """
    Collection of lessons

    `firebase.users.progress = {last_lesson}`
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


class Module(TimestampMixin):
    """
    Modules contain subcourse topics \n
    `entitled_users` This are users that have view access to module \n
    `modules_completed_users` This contains users that have complete module course \n
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=60)
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


class Lesson(TimestampMixin):
    """
    module lesson collections
    """

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=60)
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


class Question(models.Model):
    """
    Lesson question, to complete a lesson user must answer question

    To make questions dynamic we use json to store question content
    """

    class QuestionType(models.TextChoices):
        TEXT = "TEXT", "TEXT"  # simple compare text option
        DRAG_DROP = (
            "DRAG_DROP",
            "Drag Drop",
        )  # drag text options, same as text option but drag drop on ui
        TEXT_OPTIONS = (
            "TEXT_OPTION",
            "TEXT_OPTION",
        )  # compare array of strings as option
        SINGLE_CHOICE = (
            "SINGLE_CHOICE",
            "Multiple Choice",
        )  # validate single choice from multiple options
        MULTIPLE_CHOICE = (
            "MULTIPLE_CHOICE",
            "Multiple Choice",
        )  # validate more than one choice from multiple options

    title = models.CharField(max_length=60)
    content = models.JSONField()
    type = models.TextField(
        choices=QuestionType.choices,
        max_length=128,
    )

    def __str__(self) -> str:
        return self.title


class Topic(TimestampMixin):
    """
    Topic is the root representation of a course content
    """

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=128)
    content = models.TextField()
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name="topic_likes",
    )
    question = models.OneToOneField(
        Question,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    entitled_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="topic_entitled_users",
    )  # users that have access to this lesson
    topic_complete_users = models.ManyToManyField(
        User,
        blank=True,
        related_name="topic_complete_users",
    )  # user have complete this lesson

    def __str__(self):
        return self.title


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


class Category(TimestampMixin):
    """
    Collections of courses to catalogues
    """

    courses = models.ManyToManyField(Course, blank=True)
    name = models.TextField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
