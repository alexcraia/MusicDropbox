from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    key_token = models.CharField(max_length=200)
    secret_token = models.CharField(max_length=200)
    user = models.OneToOneField(User)
    request_key = models.CharField(max_length=200)
    request_secret = models.CharField(max_length=200)
    

class AllMusic(models.Model):
    file_m = models.CharField(max_length=300)
    path = models.CharField(max_length=100)
    location = models.CharField(max_length=20)
    user = models.ForeignKey(User)
