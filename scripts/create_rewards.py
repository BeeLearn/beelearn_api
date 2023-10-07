from beelearn.tests import RewardTextMixin
from reward.models import Price


def run():
    Price.objects.get_or_create(
        xp=6,
        bits=16,
        type=Price.PriceType.STREAK_COMPLETE,
    )
    Price.objects.get_or_create(
        xp=3,
        bits=8,
        type=Price.PriceType.LESSON_COMPLETE,
    )
    RewardTextMixin().create_test_rewards()

    