from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    key_token = models.CharField(max_length=200)
    secret_token = models.CharField(max_length=200)
    user = models.OneToOneField(User)
