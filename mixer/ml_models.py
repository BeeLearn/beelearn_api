from account.models import User
from catalogue.models import Course

import pandas as pd


def generate_user_model(user: User):
    """
    generate users model with
    ```
    return DataFrame(
        data = [int, list[int], list[int]],
        columns = ["userId", "categories", "tags"]
    );
    ```
    """
    categories = [category for category in user.categories.all()]
    tags = [tag.pk for category in categories for tag in category.tags]
    categories = [category.pk for category in categories]

    return pd.DataFrame(
        [user.pk, categories, tags],
        columns=["userId", "categories", "tags"],
    )


def generate_user_course_model(user: User):
    """
    generate course model with user fingerprint traces
    ```
    return DataFrame(
        data = [[int, int, list[int], list[int], bool, bool, bool, int]],
        columns = [userId, courseId, tags, categories, is_enrolled, is_completed, is_liked, average_time_spent]
    )
    ```
    """
    rows = []

    for course in Course.objects.all():
        tags = [tag for tag in course.tags.all()]
        is_liked = (
            course.modules.filter(lessons__topics__likes=user).distinct().exists()
        )
        is_enrolled = course.course_enrolled_users.contains(user)
        is_completed = course.course_complete_users.contains(user)
        average_time_spent = 0  # to fetch page average time spent from google analytics
        categories = [category for tag in tags for category in tag.category]
        tags = [tag.pk for tag in tags]

        rows.append(
            [
                user.pk,
                course.pk,
                tags,
                categories,
                is_enrolled,
                is_completed,
                is_liked,
                average_time_spent,
            ],
        )

    return pd.DataFrame(
        rows,
        columns=[
            "userId",
            "courseId",
            "is_enrolled",
            "is_completed",
            "is_liked",
            "average_time_spent",
            "tags",
            "categories",
        ],
    )
