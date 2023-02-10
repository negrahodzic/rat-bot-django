from django.utils import timezone

from django.db import models
from .managers import DiscordUserOAuth2Manager

# Create your models here.

class DiscordUser(models.Model):
    objects = DiscordUserOAuth2Manager()

    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    public_flags = models.IntegerField()
    flags = models.IntegerField()
    locale = models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)

    def is_authenticated(self, request):
        return True


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    server_id = models.IntegerField(default=123456,)
    server_name = models.CharField(default="", max_length=100)
    scrim_name = models.CharField(default="", max_length=100)  # from SheetName
    class ScrimType(models.TextChoices):
        PRO = 'pro', 'Pro'
        OPEN = 'open', 'Open'
        TOUR = 'tour', 'Tournament'

    scrim_type = models.CharField(
        max_length=4,
        choices=ScrimType.choices,
        default=ScrimType.OPEN,
    )
    # SCRIM_TYPES = (
    #     ('pro', 'Pro'),
    #     ('open', 'Open'),
    #     ('tour', 'Tournament'),
    # )
    # scrim_type = models.CharField(max_length=4, choices=SCRIM_TYPES, default='open')
    date_played = models.DateField(default=timezone.now())
    time_played = models.DateField(default=timezone.now())
    created_at = models.DateField(default=timezone.now())
    updated_at = models.DateField(default=timezone.now())
    # scores = models.DateField(default=timezone.now())
    author = models.CharField(default="author", max_length=100)  # id of person who used %sheet results last

    def __str__(self):
        return f"{self.server_name} - {self.scrim_name} - {self.scrim_type} - {self.time_played}"

    def get_scrim_type(self) -> ScrimType:
        return self.ScrimType(self.scrim_type)

class Score(models.Model):
    id = models.BigIntegerField(primary_key=True)
    rank = models.IntegerField(default=0)
    team_name = models.CharField(max_length=100)
    team_tag = models.CharField(max_length=100)
    team_managers = models.CharField(max_length=100)
    wwcd = models.IntegerField(default=0)
    pp = models.IntegerField(default=0)
    kp = models.IntegerField(default=0)
    tp = models.IntegerField(default=0)
    missed_games = models.IntegerField(default=0)
    result_id = models.ForeignKey(Result, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now())
    updated_at = models.DateField(default=timezone.now())

    def __str__(self):
        return f"#{self.rank} - {self.team_name} - {self.tp}"

# TODO:
class Server(models.Model):
    pass
class Scrim(models.Model):
    pass
class Slot(models.Model):
    pass
# class Scoreboard/SheetConfig/ResultsConfig(models.Model): ?


# OLD: scrim = models.ForeignKey(Scrim, on_delete=models.CASCADE)
