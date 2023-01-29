from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)

    bio = models.TextField(null=True)
    
    avator = models.ImageField(null=True, default='avatar.svg', upload_to='media/')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []



class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='like_post')
    
    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-date']
    
    def __str__(self):
        return self.body[0:20]


