from django.utils.timezone import now, timedelta


def get_week_start_and_end(today=None):
    """
    Get week start and end for filter based on week
    """

    if not today:
        today = now().date()

    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    return week_start, week_end
