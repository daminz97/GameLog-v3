# Generated by Django 3.2.9 on 2021-12-07 02:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_gamelog', '0016_rename_feeds_feed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='feed',
            name='value',
            field=models.FloatField(blank=True),
        ),
    ]
