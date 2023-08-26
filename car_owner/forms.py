import re
from django import forms
from user.models import UserProfile
from cars.models import Car
from django.core.exceptions import ValidationError



class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ["id", "owner", "is_booked", "capacity", "like"]
        fields = [
            "image",
            "make",
            "car_model",
            "daily_rental_price",
            "late_return_fee_per_hr",
            "ecocash_rate",
            "plate_number",
            "mileage",
            "model_year",
            "fuel_type",
            "color",
            "num_seats",
            "description",
        ]
