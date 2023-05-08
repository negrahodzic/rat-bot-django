from django.utils import timezone

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add your custom fields here
    bio = models.TextField(blank=True, null=True)
    game_username = models.CharField(max_length=20, blank=True, null=True)
    game_id = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Membership(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price} euros ({self.duration.days} days)"

class Server(models.Model):
    guild_id = models.IntegerField(unique=True)
    guild_name = models.CharField(default="", max_length=100)
    membership = models.ForeignKey(Membership, on_delete=models.RESTRICT, null=True)
    membership_start_date = models.DateTimeField(null=True, blank=True)
    membership_end_date = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='server_images/', null=True, blank=True)
    invite_link = models.CharField(default="", max_length=100)
    members = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.guild_name}"


class Result(models.Model):
    generated_by = models.CharField(default="", max_length=100)  # id of person who used %sheet results last
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

from django.contrib.auth.models import User

class Team(models.Model):
    team_name = models.CharField(max_length=30, unique=True)
    team_tag = models.CharField(max_length=10, default="")
    team_slug = models.CharField(max_length=60, unique=False, editable=False)
    team_image = models.ImageField(upload_to='team_images/', null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team_name} | {self.team_tag}"

    def save(self, *args, **kwargs):
        self.team_slug = f"{slugify(self.team_name.strip().lower())}" \
                         f"-{slugify(self.team_tag.strip().lower())}"
        super().save(*args, **kwargs)


class Score(models.Model):
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
        return f"#{self.rank} - {self.team.team_name} - {self.pp} - {self.kp} - {self.tp}"


# class Scrim(models.Model):
#     pass
#
#
# class Slot(models.Model):
#     pass

from django.db import models
from django.contrib.auth.models import User

# class Token(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     key = models.CharField(max_length=40, unique=True)
#     created = models.DateTimeField(auto_now_add=True)
