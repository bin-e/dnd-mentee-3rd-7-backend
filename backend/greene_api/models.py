from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    name = models.CharField(max_length=150, blank=True)
    first_name = None
    last_name = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'user'


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


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=150)
    date_created = models.DateTimeField(default=timezone.now)
    