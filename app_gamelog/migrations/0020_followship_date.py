# Generated by Django 3.2.9 on 2021-12-07 04:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_gamelog', '0019_auto_20211207_0353'),
    ]

    operations = [
        migrations.AddField(
            model_name='followship',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
