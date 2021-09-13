from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    public_key = models.CharField(max_length=256)
    account_id = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
