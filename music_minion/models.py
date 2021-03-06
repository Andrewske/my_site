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
    dw_monthly = models.BooleanField(default=False)
    dw_yearly = models.BooleanField(default=False)
    dw_monthly_updated_at = models.DateTimeField(null=True)
    dw_yearly_updated_at = models.DateTimeField(null=True)

    #tracks = ManyToManyField(SpotifyTrack)

    def save(self, *args, **kwargs):
        ''' Update timestamps on Save'''
        if not self.id:
            self.created_at = timezone.now()
        return super(SpotifyUser, self).save(*args, **kwargs)

    

    def __str__(self):
        return f'{self.user.username} Spotify Profile'


class SpotifyTasks(models.Model):
    task_id = models.CharField(max_length=250)
    task_name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    next_run_time = models.DateTimeField(null=True)


#class SpotifyTrack(models.Model):
#    track_id = models.CharFiels(max_length=100, null=False)
#    name = models.CharField(max_length=100, null=False)
#    tags = models.ManyToManyField(Tags)


#class Tags(models.Model):
#    name = models.CharField(max_length=100, null=False)
    

