from reward.models import Price, Reward, Streak


def run():
    Price.objects.all().delete()
    Reward.objects.all().delete()
    Streak.objects.all().delete()