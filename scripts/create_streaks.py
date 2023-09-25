from datetime import datetime, timedelta

from reward.models import Streak


def run():
    today = datetime.today()

    start = datetime(
        today.year,
        today.month,
        1,
    )

    end = datetime(
        today.year + 2,
        1,
        1,
    )

    streaks = []

    while start < end:
        streaks.append(Streak(date=start))
        start += timedelta(days=1)

    Streak.objects.bulk_create(
        streaks,
        update_conflicts=True,
        update_fields=["date"],
        unique_fields=["date"],
    )
