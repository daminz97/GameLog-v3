# Generated by Django 3.2.9 on 2021-12-07 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_gamelog', '0015_auto_20211207_0223'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Feeds',
            new_name='Feed',
        ),
    ]