from django.db import models
from .datetimeIR import *

# Create your models here.

# Define the Product model.
class Product(models.Model):
    name = models.CharField(unique=True, max_length=100)
    standard_capacity = models.IntegerField()
    adult_price = models.IntegerField()
    child_price = models.IntegerField()
    infant_price = models.IntegerField()

    def __str__(self):
        return self.name

# Define the Availability model.
class Availability(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    # Price for this date.
    price = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date}"