# Generated by Django 3.0.1 on 2020-02-09 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_minion', '0004_auto_20200208_2155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spotifyuser',
            old_name='user_id',
            new_name='user',
        ),
    ]
