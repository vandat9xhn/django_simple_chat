from django.db import models

# Create your models here.


class ProfileModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    picture = models.ImageField(upload_to='media')
