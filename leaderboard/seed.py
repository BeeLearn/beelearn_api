from beelearn.utils import file_to_image_field

from reward.models import Price

from .models import League, UserLeague


def seed_leagues():
    leagues = []

    default_price, _ = Price.objects.get_or_create(
        xp=16,
        bits=6,
        type=Price.PriceType.LEAGUE_COMPLETE,
    )

    leagues.append(
        League(
            color="#f59e0b",
            name="Mercury League",
            type=League.LeagueType.MERCURY,
            price=default_price,
        )
    )
    leagues.append(
        League(
            color="#6d28d9",
            name="Venus League",
            type=League.LeagueType.VENUS,
            price=default_price,
        )
    )

    leagues.append(
        League(
            color="#059669",
            name="Earth League",
            type=League.LeagueType.EARTH,
            price=default_price,
        )
    )

    leagues.append(
        League(
            color="#b91c1c",
            name="Mars League",
            type=League.LeagueType.MARS,
            price=default_price,
        )
    )

    leagues.append(
        League(
            color="#1d4ed8",
            name="Jupiter League",
            type=League.LeagueType.JUPITER,
            price=default_price,
        )
    )

    leagues.append(
        League(
            color="#6d28d9",
            name="Saturn League",
            type=League.LeagueType.SATURN,
            price=default_price,
        )
    )

    for league in leagues:
        if not League.objects.filter(type=league.type).exists():
            league.icon = file_to_image_field(
                f"leaderboard/static/leagues/{league.type.lower()}.webp"
            )

    League.objects.bulk_create(
        leagues,
        update_conflicts=True,
        unique_fields=["type"],
        update_fields=[
            "name",
            "color",
        ],
    )


def up():
    seed_leagues()


def down():
    League.objects.all().delete()
    UserLeague.objects.all().delete()
