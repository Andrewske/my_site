# Generated by Django 3.0.1 on 2020-03-29 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_minion', '0006_auto_20200329_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='spotifyuser',
            name='dw_updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]