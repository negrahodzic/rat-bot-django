# Generated by Django 4.1.3 on 2022-11-10 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ratbotapp', '0010_remove_discorduser_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scrim',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('server_id', models.IntegerField()),
                ('server_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=100)),
                ('team_tag', models.CharField(max_length=100)),
                ('team_managers', models.CharField(max_length=100)),
                ('rank', models.IntegerField(default=0)),
                ('wwcd', models.IntegerField(default=0)),
                ('pp', models.IntegerField(default=0)),
                ('kp', models.IntegerField(default=0)),
                ('tp', models.IntegerField(default=0)),
                ('missed_games', models.IntegerField(default=0)),
                ('scrim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ratbotapp.scrim')),
            ],
        ),
    ]
