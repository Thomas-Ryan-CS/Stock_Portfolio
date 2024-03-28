from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    value = models.DecimalField(max_digits=10, decimal_places=2)