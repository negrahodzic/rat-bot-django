# Generated by Django 4.1.6 on 2023-02-13 09:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratbotapp', '0003_alter_result_created_at_alter_result_date_played_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 13, 9, 13, 56, 478750, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='result',
            name='date_played',
            field=models.DateField(default=datetime.datetime(2023, 2, 13, 9, 13, 56, 478750, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='result',
            name='time_played',
            field=models.DateField(default=datetime.datetime(2023, 2, 13, 9, 13, 56, 478750, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='result',
            name='updated_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 13, 9, 13, 56, 478750, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='score',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 13, 9, 13, 56, 479707, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='score',
            name='updated_at',
            field=models.DateField(default=datetime.datetime(2023, 2, 13, 9, 13, 56, 479707, tzinfo=datetime.timezone.utc)),
        ),
    ]
