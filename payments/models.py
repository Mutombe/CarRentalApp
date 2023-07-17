from django.db import models
from cars.models import Car
from rental.models import Rental
#from user.models import Customer

class Payment(models.Model):
    rental = models.ForeignKey(Rental,on_delete=models.CASCADE)
    #customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.ForeignKey(Car, on_delete=models.CASCADE)
