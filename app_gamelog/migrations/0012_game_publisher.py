# Generated by Django 3.2.9 on 2021-12-06 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_gamelog', '0011_user_is_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='publisher',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
