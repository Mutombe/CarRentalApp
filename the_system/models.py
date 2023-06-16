from django.db import models
from decimal import Decimal
from django.db import models
#from user.models import Account
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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

def customer_age(value):
    if value <= 19:
        raise ValidationError(
            _(f'{value} is too young, you must be older than 19'),
            params={'value': value},
        )

#def drivers_licence(value):
 #   if value <= 0:
  #      raise ValidationError(
   #         _(f'{value} is to small, it must be greater than 0'),
    #        params={'value': value},
     #   )

def validate_num_of_passengers(value):
    if value > 4:
        raise ValidationError(
            _(f'{value} is too much passengers, it must be less than 5'),
            params={'value': value},
        )

#---------------------------------------------------------------------------------------------------------------------
class Location(models.Model):
    city = models.CharField(max_length=100, null=False, blank=False)
    place = models.CharField(max_length=100, null=False, blank=False)
    Avenue = models.CharField(max_length=200, null=True, blank=True)
    house_number = models.IntegerField(null=False, blank=False)
    postal_code = models.IntegerField(null=True, blank=True)
    proof_of_residence = models.ImageField(
        upload_to='static/images', 
        null=False, 
        blank=False
        )

    def __str__(self):
        return self.city
#----------------------------------------------------------------------------------------------------------------------------
class carOwner (models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)   
    #account = models.ForeignKey(Account, on_delete=models.CASCADE)
    address = models.ForeignKey(Location, on_delete=models.CASCADE)
    contact = models.IntegerField(null=False, blank=True)
    profile_image = models.ImageField(
        upload_to='static/images', 
        blank=False, 
        null=False
        )
    social_media_account = models.SlugField(max_length=100)
    number_of_cars = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.username, self.lastname
#------------------------------------------------------------------------------------------------------------------------------
class Car (models.Model):
    booking_days_choices = [
        ("1", "1_DAY"),
        ("2", "2_DAY"),
        ("3", "3_DAY"),
        ("4", "4_DAY"),
        ("5", "5_DAY"),
    ]

    categories = [
        ("P", "Petrol"),
        ("D", "Diesel"),
        ("G", "Gas"),
        ("H", "Hybrid"),
        ("E", "Electric"),
    ]

    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=20)
    photos = models.ImageField(
        upload_to='static/images', 
        blank=False, 
        null=False
        )
    model_year = models.IntegerField(default=0, validators=[validate_year])
    color = models.CharField(max_length=20, blank= False)
    num_of_passengers = models.PositiveSmallIntegerField(
        null=False, 
        blank=False, 
        validators=[validate_num_of_passengers]
        )
    capacity = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=7, blank=False)
    owner = models.ForeignKey(carOwner, on_delete=models.CASCADE)
    booked = models.BooleanField()
    rental_price = models.DecimalField(
        decimal_places=2, 
        max_digits=6, 
        default=Decimal("0.00"),
        validators=[daily_rental_cost]
        )
    booking_days = models.CharField(
        max_length=20, 
        choices=booking_days_choices,
        blank=False, 
        null=False
        )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    car_engine = models.PositiveSmallIntegerField(
        choices=categories, 
        blank=False, 
        validators=[validate_car_engine_power]
        )

    def __str__(self):
        return self.brand
#----------------------------------------------------------------------------------------------------------------
class Customer(models.Model):
    username = models.CharField(max_length=50)
   # account = models.ForeignKey(Account, on_delete=models.CASCADE)
    contact = models.IntegerField(null=False, blank=True)
    address = models.ForeignKey(Location, on_delete=models.CASCADE)
    car_selected = models.ForeignKey(Car, on_delete=models.CASCADE)
    booking_history = models.CharField(max_length=40)

    def __str__(self):
        return self.username
#--------------------------------------------------------------------------------------------------------------    
class Rental(models.Model):
    choices_for_status = [
        ('1', 'In_progress'),
        ('2', 'Due'),
    ]

    rental_date = models.DateField(verbose_name="date rented", auto_now_add=True)
    rental_time = models.TimeField(verbose_name="time rented")
    return_date = models.DateField(verbose_name="return date")
    car_owner = models.ForeignKey(carOwner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rental_status = models.CharField(
        max_length=100, 
        choices=choices_for_status
        )

    def __str__(self):
        return self.car

#----------------------------------------------------------------------------------------------------------------------
class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(
        decimal_places=2, 
        max_digits=6, 
        verbose_name="payment amount", 
        null=False, 
        blank=False
        )
    payment_date = models.DateField(null=False, auto_now_add=True)

    def __str__(self):
        return self.rental

#---------------------------------------------------------------------------------------------------------------------
class CarReview(models.Model):
    review_choices = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ]

    review_score = models.CharField(
        max_length=30,
        choices=review_choices, 
        null=False, 
        blank=False
        )
    date = models.DateField(null=False, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    owner = models.ForeignKey(carOwner, on_delete=models.CASCADE)

    def __str__(self):
        return self.review_score

#--------------------------------------------------------------------------------------------------------------------------
class Booking (models.Model):
    confirmation_number = models.IntegerField(auto_created=True)
    username = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    booking_startdate = models.DateField(null=False)
    booking_enddate = models.DateField(null=False)
    booking_duration = models.DurationField(blank=False)
    amount_paid = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=False,
        )
    def __str__(self):
        return self.username
