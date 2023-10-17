from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from user.models import CustomUser


class Chauffeur(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    profile_photo = models.ImageField(
        upload_to="static/media/chauffeur_profiles", blank=False
    )
    first_name = models.CharField(max_length=50, null=False, blank=False, default=None)
    last_name = models.CharField(max_length=50, null=False, blank=False, default=None)
    phone_number = models.IntegerField(default="+263")
    email = models.EmailField(blank=False, default=None)
    daily_fee = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        default=Decimal("0.00"),
    ) 
    driver_experience = models.PositiveIntegerField(default=None)
    ecocash_rate = models.DecimalField(
        default=Decimal("0.00"), max_digits=7, decimal_places=2
    )
    is_booked = models.BooleanField(default=False)
    rating = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
        ],
    )
    date_joined = models.DateTimeField(default=timezone.now)
