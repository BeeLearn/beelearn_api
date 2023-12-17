from django.db.models import Count, OuterRef, Exists

from account.models import User

from catalogue.models import Course, Category, Topic


def generate_user_category_feed(user: User = None):
    categories = [
        {
            "name": "Today's Pick",
            "description": "Recommendations Based on your previous activities",
            "model": legacy_today_pick,
        },
        {
            "name": "Popular now",
            "description": "Trending from interest",
            "model": legacy_popular_now,
        },
        {
            "name": "Current Favorite",
            "description": "Your favourite courses",
            "model": legacy_current_favorites,
        },
        {
            "name": "Feature Today",
            "description": "Hand picked by our curators just for you",
            "model": legacy_featured_today,
        },
    ]

    save_categories = []

    for category in categories:
        if not user:
            for user in User.objects.all():
                save_categories.append(generate_feed(category, user))
        else:
            save_categories.append(generate_feed(category, user))


def generate_feed(detail: dict, user: User):
    category, _ = Category.objects.update_or_create(
        {
            "name": detail["name"],
        },
        description=detail["description"],
        user=user,
    )

    courses = detail["model"](user).only("pk").values_list("pk")
    category.courses.add(*[course[0] for course in courses])

    return category


def legacy_today_pick(user: User):
    return (
        Course.objects.exclude(course_complete_users=user)
        .exclude(is_visible=False)
        .exclude(course_enrolled_users=user)
        .filter(tags__category__in=user.categories.all())
        .order_by("?")
    )


def legacy_popular_now(user: User):
    return (
        Course.objects.annotate(enrolled_users_count=Count("course_enrolled_users"))
        .exclude(is_visible=False)
        .filter(
            tags__category__in=user.categories.all(),
        )
        .order_by(
            "-enrolled_users_count",
            "-created_at",
        )
    )


def legacy_current_favorites(user: User):
    courses = (
        Course.objects.exclude(is_visible=False)
        .filter(course_enrolled_users=user)
        .annotate(
            is_liked=Exists(
                Topic.objects.filter(
                    lesson__module__course=OuterRef("pk"),
                )
            )
        )
        .filter(is_liked=True)
        .order_by("-updated_at")
    )

    return courses


# todo make featured today
# courses added less than a week
def legacy_featured_today(user: User):
    return (
        Course.objects.exclude(course_complete_users=user)
        .exclude(is_visible=False)
        .order_by("?")
    )
