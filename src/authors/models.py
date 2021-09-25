from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    name = models.CharField(max_length=20)
    kind = models.CharField(max_length=50, default='')
    publickey = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
