from django.db import models
from cars.models import Car
from rental.models import Rental

class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    ecocash = models.BooleanField(default=False)
    usd = models.BooleanField(default=True)
