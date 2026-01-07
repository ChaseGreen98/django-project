from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Computer(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='computers',
    )
    cpu = models.CharField(max_length=100, null=True)
    motherboard = models.CharField(max_length=100, null=True)
    gpu = models.CharField(max_length=100, null=True)
    ram = models.CharField(max_length=100, null=True)
    storage = models.CharField(max_length=100, null=True)
    cooler = models.CharField(max_length=100, null=True)
    psu = models.CharField(max_length=100, null=True)
    case = models.CharField(max_length=100, null=True)
    price = models.IntegerField()
    