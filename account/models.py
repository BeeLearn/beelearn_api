from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from beelearn.models import TimestampMixin
from catalogue.models import Course, Lesson

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    xp = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        default=3,
    )  # experience point

    def __str__(self):
        return self.email


class UserCourse(TimestampMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    last_lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.course.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "user"],
                name="User can have only one unique course saved",
            )
        ]
