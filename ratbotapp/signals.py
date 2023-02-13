from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from ratbotapp.models import Team


@receiver(pre_save, sender=Team)
def set_team_slug(sender, instance, **kwargs):
    instance.team_slug = f"{slugify(instance.team_name.strip().lower())}-{slugify(instance.team_tag.strip().lower())}"
