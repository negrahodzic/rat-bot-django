# Generated by Django 4.1.3 on 2022-11-09 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratbotapp', '0009_discorduser_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discorduser',
            name='password',
        ),
    ]