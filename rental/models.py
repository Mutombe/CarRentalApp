from django.db import models
from cars.models import Car
#from user.models import Car_Owner


class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    renter_name = models.CharField(max_length=50)
    #car_owner = models.ForeignKey(Car_Owner,on_delete=models.CASCADE)
    renter_address = models.CharField(max_length=100)
    renter_phone = models.CharField(max_length=20)
    renter_email = models.EmailField()
    driver_license = models.ImageField(upload_to='driver_license/')
    credit_card_number = models.CharField(max_length=20)
    credit_card_expiration = models.CharField(max_length=7)
    credit_card_security_code = models.CharField(max_length=4)
    rental_period = models.PositiveIntegerField()
    rental_start_date = models.DateField(auto_now_add=True)
    rental_end_date = models.DateField()