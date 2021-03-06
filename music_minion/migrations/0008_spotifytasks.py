# Generated by Django 3.0.1 on 2020-03-29 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music_minion', '0007_spotifyuser_dw_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dw_monthly', models.BooleanField(default=False)),
                ('dw_yearly', models.BooleanField(default=False)),
                ('dw_updated_at', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='music_minion.SpotifyUser')),
            ],
        ),
    ]
