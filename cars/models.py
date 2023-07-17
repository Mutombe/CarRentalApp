from django.db import models
from django.shortcuts import reverse
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser

def validate_year(value):
    if value < 2000:
        raise ValidationError(
            _(f'{value} this year is not supported, it must be greater than 2000'),
            params= {'value': value},
        )

def validate_car_engine_power(value):
    if value <= 0:
        raise ValidationError(
            _(f'{value} is too small, it must be greater than 0'),
            params={'value': value},
        )

def daily_rental_cost(value):
    if value <= 0:
        raise ValidationError(
            _(f'{value} is to small, it must be greater than 0'),
            params={'value': value},
        )


def validate_num_of_passengers(value):
    if value > 4:
        raise ValidationError(
            _(f'{value} is too much passengers, it must be less than 5'),
            params={'value': value},
        )
        
def car_photo_upload_path(instance, filename):
    return f'static/media/cars/{instance.owner.username}/{filename}'

class Car(models.Model):
    categories = [
        ("P", "Petrol"),
        ("D", "Diesel"),
        ("G", "Gas"),
        ("H", "Hybrid"),
        ("E", "Electric"),
    ]

    id = models.AutoField(null=False, primary_key=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None)
    make = models.CharField(max_length=50, null=False, blank=False)
    car_model = models.CharField(max_length=20, null=False, blank=False)
    model_year = models.IntegerField(default=0, validators=[validate_year])
    color = models.CharField(max_length=20, blank= False)
    num_seats = models.PositiveSmallIntegerField(null=False, blank=False, validators=[validate_num_of_passengers])
    capacity = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=7, blank=False)
    is_booked = models.BooleanField(default=False)
    has_tracker = models.BooleanField(default=False)
    daily_rental_price = models.DecimalField(decimal_places=2, max_digits=6, default=Decimal("0.00"),validators=[daily_rental_cost])
    late_return_fee_per_hr = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal("0.00"),null=True, blank=True)
    mileage = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=1, choices=categories)
    like = models.IntegerField(default=0)
    description = models.CharField(max_length=500,null=True, default=True)

    def __str__(self):
        return self.make

    def get_url(self):
        return reverse('car_detail', args = (self.id))
    
      


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="photos")
    image = models.FileField(upload_to=car_photo_upload_path , blank=False, default='/static/media/images/logo.png')
    
    
    def get_image(self, index=0):
        if index < len(self.photo):
            return self.photo[index]
        else:
            return None

class CarsReservationHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    day1 = models.DateTimeField()
    day2 = models.DateTimeField()
    day3 = models.DateTimeField()
    day4 = models.DateTimeField()
    day5 = models.DateTimeField()

    class Meta:
        verbose_name = "CarHistory"
        verbose_name_plural = "CarsHistory"

    def __int__(self):
        return self.car

