from decimal import Decimal
from django.db import models
from cars.models import Car
from django.urls import reverse
from user.models import CustomUser
from chauffeur.models import Chauffeur


class Rental(models.Model):
    RENTAL_STATUS = [
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    PAYMENT_METHOD_CHOICES = [("Ecocash", "Ecocash"), ("USD", "USD")]
   
    id = models.AutoField(null=False, primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=PAYMENT_METHOD_CHOICES,
        default="USD",
    )
    chauffeur = models.ForeignKey(
        Chauffeur, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    with_chauffeur = models.BooleanField(default=False)
    customer_destination = models.CharField(max_length=100, blank=False, default=None)
    status = models.CharField(max_length=100, choices=RENTAL_STATUS, default=None)
    is_returned = models.BooleanField(default=False)
    return_date = models.DateField(blank=True, null=True)
    rental_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )
    late_return_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    #def calculate_rental_fee(self):
     #   rental_days = (self.end_date - self.start_date).days + 1
      #  if self.car.ecocash_rate and self.payment_method == "Ecocash":
       #     rental_fee = (
        #        self.car.daily_rental_price * rental_days * self.car.ecocash_rate
         #   )
        #elif self.chauffeur.ecocash_rate and self.payment_method == "Ecocash":
         #   if self.with_chauffeur:
          #      rental_fee = self.car.daily_rental_price * self.car.ecocash_rate + (
           #         self.chauffeur.ecocash_rate * self.chauffeur.daily_fee
            #    )
        #elif self.payment_method == "USD" and self.with_chauffeur:
         #   rental_fee = rental_days * (
          #      self.car.daily_rental_price + self.chauffeur.daily_fee
           # )
        #else:
         #   rental_fee = self.car.daily_rental_price * rental_days
        #return rental_fee

    # def calculate_grand_total(self, payment_method):
    #    rental_fee = self.calculate_rental_fee()
    #    if self.return_date and self.return_date > self.end_date:
    #        late_return_fee = self.car.late_return_fee_per_hr * (
    #                (self.return_date - self.end_date).seconds // 3600
    #            )

    #    elif self.return_date and self.return_date > self.end_date:
    #        if self.payment_method == 'Ecocash':
    #            late_return_fee =  self.car.ecocash_rate * (
    #                                            self.car.late_return_fee_per_hr *
    #                                            ((self.return_date - self.end_date).seconds // 3600)
    #                                        )
    #            total = late_return_fee + rental_fee
    #    return total

    def get_absolute_url(self):
        return reverse("rental_detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.customer.username} rented {self.car.make} {self.car.car_model}"


class RentalHistory(models.Model):
    car_owner = models.CharField(max_length=100, default=None, blank=False)
    customer = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, blank=False, default=None
    )
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT, default=None, blank=False)
    rental_days = models.IntegerField(blank=False, default=None)
    chauffeurs_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
