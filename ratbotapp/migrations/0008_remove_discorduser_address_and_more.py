# Generated by Django 4.1.3 on 2022-11-09 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratbotapp', '0007_discorduser_has_module_perms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discorduser',
            name='Address',
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='Landmark',
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='Mobile',
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='Status',
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='has_module_perms',
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='is_staff',
        ),
    ]
