# Generated by Django 4.1.3 on 2022-11-09 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratbotapp', '0005_discorduser_address_discorduser_landmark_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discorduser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
