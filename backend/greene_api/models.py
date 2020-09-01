from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    class Meta:
        db_table = "user"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    like = models.IntegerField(default=0)
    thumbnail = models.ImageField(
        default='thumbnail_images/default_image.jpeg',
        upload_to='thumbnail_images/'
        )
    hashtags = models.ManyToManyField('hashtag')
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.title}"


class Hashtag(models.Model):
    name = models.CharField(max_length=150)
