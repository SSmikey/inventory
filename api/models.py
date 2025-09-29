from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TYPE_CHOICES = (("in","IN"), ("out","OUT"))
    id = models.CharField(max_length=36, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transactions")
    quantity = models.IntegerField()
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    total_price = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
