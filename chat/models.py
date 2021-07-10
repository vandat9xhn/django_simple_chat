from django.db import models
#
from account.models import ProfileModel

# Create your models here.


class Room(models.Model):
    name = models.CharField(unique=True, max_length=100)


class Message(models.Model):
    room_model = models.ForeignKey(Room, on_delete=models.CASCADE)
    profile_model = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='ms_prf')
    message = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    message_model = models.ForeignKey(Message, on_delete=models.CASCADE)
    image = models.ImageField()
