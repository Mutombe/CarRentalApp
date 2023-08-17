from django.db import models
from django.shortcuts import reverse
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser
from django.utils import timezone


def daily_rental_cost(value):
    if value <= 0:
        raise ValidationError(
            _(f"{value} is to small, it must be greater than 0"),
            params={"value": value},
        )


def validate_num_of_passengers(value):
    if value > 8:
        raise ValidationError(
            _(f"{value} is too much passengers, it must be less than 8"),
            params={"value": value},
        )


def car_photo_upload_path(instance, filename):
    return f"static/media/cars/{instance.owner.username}/{filename}"


class Car(models.Model):
    categories = [
        ("Petrol", "Petrol"),
        ("Diesel", "Diesel"),
        ("Gas", "Gas"),
        ("Hybrib", "Hybrid"),
        ("Electric", "Electric"),
    ]

    id = models.AutoField(null=False, primary_key=True)
    image = models.ImageField(
        upload_to="static/media/cars/images",
        blank=False,
        default="/static/media/cars/images/logo.png",
    )
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=False
    )
    make = models.CharField(max_length=50, null=False, blank=False)
    car_model = models.CharField(max_length=20, null=False, blank=False)
    city = models.CharField(max_length=100, null=True, blank=False)
    residence = models.CharField(max_length=100, null=True, blank=False)
    model_year = models.IntegerField(default=0)
    color = models.CharField(max_length=20, blank=False)
    num_seats = models.PositiveSmallIntegerField(
        null=False, blank=False, validators=[validate_num_of_passengers]
    )
    capacity = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=7, blank=False)
    is_booked = models.BooleanField(default=False)
    has_tracker = models.BooleanField(default=False)
    daily_rental_price = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        default=Decimal("0.00"),
        validators=[daily_rental_cost],
    )
    late_return_fee_per_hr = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00"), null=True, blank=True
    )
    ecocash_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00"), null=True, blank=True
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=10, choices=categories)
    like = models.IntegerField(default=0)
    description = models.CharField(max_length=500, null=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)
    is_saved = models.BooleanField(default=False)

    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dis_likes(self):
        return self.dis_likes.users.count()

    def __str__(self):
        return self.make

    def get_url(self):
        return reverse("car_detail", args=(self.id))

    # def get_image(self, index=0):
    #   if index < len(self.image):
    #      return self.image[index]
    # else:
    #    return None


class SavedCar(models.Model):
    car = models.ForeignKey(Car, related_name="cars", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="saved", on_delete=models.CASCADE)
    date_saved = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "car")

    def __str__(self):
        return self.car.make


class Like(models.Model):
    """like  car"""

    car = models.OneToOneField(Car, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(CustomUser, related_name="requirement_car_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.car.make)[:30]


class DisLike(models.Model):
    """Dislike  car"""

    car = models.OneToOneField(Car, related_name="dis_likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(CustomUser, related_name="requirement_car_dis_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.car.make)[:30]
