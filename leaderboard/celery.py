from .models import League, UserLeague


def league_demotion_or_promotion_job():
    leagues = League.objects.all()

    for league in leagues:
        for group in league.groups():
            promoted = group[: int(0.3 * len(group))]
            stagnated = group[int(0.3 * len(group)) : int(0.7 * len(group))]
            demoted = group[-int(0.3 * len(group)) :]

            updates = []

            for promotion in promoted:
                index = League.LeagueRanking.index(promotion.league.type)

                if index < len(League.LeagueRanking):
                    group.league = League.LeagueRanking[index + 1]

                group.xp = 0
                group.xp_before = group.user.profile.xp

                updates.append(group)

            for stagnate in stagnated:
                group.xp = 0
                group.xp_before = group.user.profile.xp

                updates.append(group)

            for demotion in demoted:
                index = League.LeagueRanking.index(demotion.league.type)

                if index != 0:
                    group.league = League.LeagueRanking[index - 1]

                group.xp = 0
                group.xp_before = group.user.profile.xp

                updates.append(group)

            UserLeague.objects.bulk_update(
                updates,
                ["xp", "xp_before", "league"],
            )
