from django.utils import timezone

from django.db import models
from django.utils.text import slugify

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


class Membership(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price} euros ({self.duration.days} days)"

class Server(models.Model):
    id = models.AutoField(primary_key=True)
    guild_id = models.IntegerField(unique=True)
    guild_name = models.CharField(default="", max_length=100)
    membership = models.ForeignKey(Membership, on_delete=models.RESTRICT, null=True)
    membership_start_date = models.DateTimeField(null=True, blank=True)
    membership_end_date = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='server_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.guild_name}"


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.CharField(default="", max_length=50)  # id of person who used %sheet results last
    server = models.ForeignKey(Server, on_delete=models.RESTRICT, default=None)
    scrim_name = models.CharField(default="", max_length=100)

    # scoring_system_id

    class ScrimType(models.TextChoices):
        PRO = 'pro', 'Pro'
        OPEN = 'open', 'Open'
        TOUR = 'tour', 'Tournament'

    scrim_type = models.CharField(
        max_length=4,
        choices=ScrimType.choices,
        default=ScrimType.OPEN,
    )

    date_played = models.DateField()
    time_played = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.scrim_name} - {self.time_played} ({self.scrim_type})"

    def get_scrim_type(self) -> ScrimType:
        return self.ScrimType(self.scrim_type)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_played = timezone.now().date()
        super().save(*args, **kwargs)


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=30, unique=True)
    team_tag = models.CharField(max_length=10, default="")
    team_slug = models.CharField(max_length=60, unique=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team_name} | {self.team_tag}"

    def save(self, *args, **kwargs):
        self.team_slug = f"{slugify(self.team_name.strip().lower())}-{slugify(self.team_tag.strip().lower())}"
        super().save(*args, **kwargs)


class Score(models.Model):
    id = models.AutoField(primary_key=True)
    rank = models.IntegerField(default=0)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, default=None)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, default=None)
    team_managers = models.CharField(max_length=200, default='Unknown')
    wwcd = models.PositiveSmallIntegerField(default=0)
    pp = models.PositiveSmallIntegerField(default=0)
    kp = models.PositiveSmallIntegerField(default=0)
    tp = models.PositiveSmallIntegerField(default=0)
    missed_games = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.rank} - {self.team.team_name} - {self.tp}"


class Scrim(models.Model):
    pass


class Slot(models.Model):
    pass
# class Scoreboard/SheetConfig/ResultsConfig(models.Model): ?


# OLD: scrim = models.ForeignKey(Scrim, on_delete=models.CASCADE)
