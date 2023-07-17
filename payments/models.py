from django.db import models
from cars.models import Car
from rental.models import Rental
from user.models import CustomUser

class Payment(models.Model):
    rental = models.ForeignKey(Rental,on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.ForeignKey(Car, on_delete=models.CASCADE)
