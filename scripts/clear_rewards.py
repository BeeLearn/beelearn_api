from reward.models import Price, Reward


def run():
    Price.objects.all().delete()
    Reward.objects.all().delete()