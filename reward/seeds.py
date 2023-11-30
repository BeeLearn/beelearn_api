from beelearn.utils import file_to_image_field

from .models import Price, Reward


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

    default_price, _ = Price.objects.get_or_create(
        xp=12,
        bits=6,
        type=Price.PriceType.REWARD_ACHIEVE,
    )

    rewards = [
        Reward(
            type=Reward.RewardType.VERIFY_ACCOUNT,
            title="Verify Account",
            description="Verify your account's email address",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.JUST_GETTING_STARTED,
            title="Just getting started",
            description="Complete first lesson of a course",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.COURSE_MASTER,
            title="Course master",
            description="Complete a course",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.COURSE_NINJA,
            title="Course ninja",
            description="Complete then courses in a row",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.HAT_TRICK,
            title="Hat trick",
            description="Complete three courses in a row",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.WE_ARE_IN_THIS_TOGETHER,
            title="We are in this together",
            description="Comment on a topic or lesson more than 2 times",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.ENGAGED_IN,
            title="Engaged in",
            description="Comment on a course more than 10 times",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.FEARLESS,
            title="Fearless",
            description="Complete a rare challenge",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.NEW_CAREER_AWAITS,
            title="New career awaits",
            description="Make use of your skills in a unique way",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.WHERE_THE_MAGIC_HAPPENS,
            title="Where the magic happens",
            description="Complete a modules in a course",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
        Reward(
            type=Reward.RewardType.ACHIEVER,
            title="Achiever",
            description="Complete a rare challenge",
            color="0xFF43A047",
            dark_color="0xFF2D3035",
            price=default_price,
        ),
    ]

    for reward in rewards:
        if not Reward.objects.filter(type=reward.type).exists():
            reward.icon = file_to_image_field(
                f"reward/static/rewards/{reward.type.lower()}.png"
            )

    Reward.objects.bulk_create(
        rewards,
        update_conflicts=True,
        update_fields=[
            "title",
            "description",
            "color",
            "dark_color",
            "price",
        ],
        unique_fields=["type"],
    )

    return rewards
