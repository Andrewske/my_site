# Generated by Django 3.0.1 on 2020-03-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_minion', '0005_auto_20200208_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='spotifyuser',
            name='dw_monthly',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spotifyuser',
            name='dw_yearly',
            field=models.BooleanField(default=False),
        ),
    ]
