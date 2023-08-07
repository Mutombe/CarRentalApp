from django.forms import ModelForm
from .models import Car
from django import forms


class CarsForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "make",
            "car_model",
            "num_seats",
            "daily_rental_price",
            "description",
        ]      


