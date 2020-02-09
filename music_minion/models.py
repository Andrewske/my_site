from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class SpotifyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(editable=False)
    auth_date = models.DateTimeField()
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        ''' Update timestamps on Save'''
        if not self.id:
            self.created_at = timezone.now()
        self.auth_date = timezone.now()
        return super(SpotifyUser, self).save(*args, **kwargs)

    

    def __str__(self):
        return f'{self.user.username} Spotify Profile'

