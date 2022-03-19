from __future__ import unicode_literals
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=40, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.IntegerField()
