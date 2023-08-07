from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from user.models import CustomUser

class Chauffeur(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    id = models.AutoField(primary_key=True)
    profile_photo = models.ImageField(upload_to="static/media/chauffeur_profiles", blank=False, default="static/media/chauffeur_profiles/default_prof_pic.png")
    first_name = models.CharField(max_length=50, null=False, blank=False, default=None)
    last_name = models.CharField(max_length=50, null=False, blank=False, default=None)
    phone_number = models.IntegerField(default='+263')
    email = models.EmailField(blank=False, default=None)
    daily_fee = models.DecimalField(decimal_places=2, max_digits=6, default=Decimal("0.00"), )#validators=[validate_chauffeur_fee]
    driver_experience = models.PositiveIntegerField(default=None)
    ecocash_rate = models.DecimalField(default=0.0 ,max_digits=5, decimal_places=2)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0),])

