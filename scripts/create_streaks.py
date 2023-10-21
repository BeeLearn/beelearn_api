from datetime import datetime, timedelta

from reward.models import Streak


def run():
    today = datetime.today()
    end = datetime(
        today.year + 2,
        1,
        1,
    )

    streaks = []

    while today < end:
        streaks.append(Streak(date=today))
        today += timedelta(days=1)

    Streak.objects.bulk_create(
        streaks,
        update_conflicts=True,
        update_fields=["date"],
        unique_fields=["date"],
    )
