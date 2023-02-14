import os

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from ratbotapp.models import Team, Server


@receiver(pre_save, sender=Team)
def set_team_slug(sender, instance, **kwargs):
    instance.team_slug = f"{slugify(instance.team_name.strip().lower())}-{slugify(instance.team_tag.strip().lower())}"


@receiver(pre_save, sender=Server)
def rename_profile_image(sender, instance, **kwargs):
    # generate new file name
    file_extension = os.path.splitext(instance.profile_image.name)[1]
    new_file_name = f"server_profile_image_{instance.guild_id}{file_extension}"

    # update file name
    instance.profile_image.name = new_file_name