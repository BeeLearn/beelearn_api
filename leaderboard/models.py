from django.db import models
from django.utils import timezone
from django.db.models.manager import BaseManager

from account.models import User

from reward.models import Price

from .utils import group


class League(models.Model):
    MAX_LEAGUE_MEMBERS = 24

    user_leagues: BaseManager["UserLeague"]

    class LeagueType(models.TextChoices):
        MARS = "MARS", "Mars"
        VENUS = "VENUS", "Venus"
        EARTH = "EARTH", "Earth"
        SATURN = "SATURN", "Saturn"
        MERCURY = "MERCURY", "Mercury"
        JUPITER = "JUPITER", "Jupiter"

        # PLUTO = "PLUTO", "Pluto"
        # URANUS = "URANUS", "Uranus"
        # NEPTUNE = "NEPTUNE", "Neptune"

    LeagueRanking = [
        LeagueType.MERCURY,
        LeagueType.VENUS,
        LeagueType.EARTH,
        LeagueType.MARS,
        LeagueType.JUPITER,
        LeagueType.SATURN,
        # LeagueType.URANUS,
        # LeagueType.NEPTUNE,
        # LeagueType.PLUTO,
    ]

    name = models.TextField()
    color=models.CharField(max_length=8)
    type = models.TextField(
        choices=LeagueType.choices,
        unique=True,
    )
    icon = models.ImageField(
        upload_to="assets/leagues/icons",
    )
    users = models.ManyToManyField(
        User,
        blank=True,
        through="UserLeague",
    )
    price = models.ForeignKey(
        Price,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    @property
    def groups(self):
        user_leagues = self.user_leagues.all()
        return group(
            user_leagues,
            self.MAX_LEAGUE_MEMBERS,
        )
    
    def __str__(self):
        return self.name


class UserLeague(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name="user_leagues",
    )
    xp = models.IntegerField(default=0)
    xp_before = models.IntegerField(default=0)

    created_at = models.DateTimeField(
        default=timezone.now,
        auto_created=True,
    )

    class Meta:
        ordering = ["-xp_before"]
