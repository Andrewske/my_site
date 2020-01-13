from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


class Technologies(models.Model):
    title = models.CharField(max_length=100)
    comfort = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='tech_icons')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
