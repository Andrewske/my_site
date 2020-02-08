from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class SpotifyUser(models.Model):
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    auth_date = models.DateTimeField(default=timezone.now)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Spotify Profile'

