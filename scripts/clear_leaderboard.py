from leaderboard.models import League, UserLeague


def run():
    League.objects.all().delete()
    UserLeague.objects.all().delete()
