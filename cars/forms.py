from django.forms import ModelForm
from .models import Car, SavedCar
from django import forms


class SaveCarForm(forms.ModelForm):
    class Meta:
        model = SavedCar
        fields = ["car", "user"]
