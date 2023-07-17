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
    [firebase.users.progress] = {last_lesson}
    """

    COURSE_IMAGE_PATH = Path("assets/courses")

    name = models.TextField(max_length=128)
    image = models.ImageField(upload_to=COURSE_IMAGE_PATH / "backgrounds")

    def __str__(self):
        return self.name


class Topic(TimestampMixin):
    """
    SubTopics
    """


class Question(models.Model):
    """ """

    title = models.CharField(max_length=60)
    question = models.JSONField()
    answer = models.JSONField()

    def __str__(self) -> str:
        return self.title


class Lesson(TimestampMixin):
    """
    Lesson is the root representation of a course content
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    title = models.TextField(max_length=128)
    description = models.TextField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Lesson detailed description (Optional)",
    )
    content = models.TextField()
    likes = models.ManyToManyField(
        User,
        blank=True,
    )
    question = models.OneToOneField(
        Question,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class LessonComment(TimestampMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
    )
    comment = models.TextField()

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
