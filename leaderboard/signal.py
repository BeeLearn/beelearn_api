from django.dispatch import receiver
from django.db.models.signals import post_save


from account.models import User

from .models import League, UserLeague


@receiver(signal=post_save, sender=User)
def user_post_save(instance: User, **kwargs):

    if not instance.userleague:
        UserLeague.objects.create(
            user=instance,
            league=League.objects.get(
                type=League.LeagueRanking[0],
            ),
            xp_before=instance.profile.xp,
        )
