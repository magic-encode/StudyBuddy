from django.db import models

# Create your models here.


class Room(models.Model):
    # topic = 
    name = models.CharField(max_length=200)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    
