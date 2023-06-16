import datetime
from django import forms
from django.forms import ModelForm

from .models import Car

class CarForm(ModelForm):
    model = Car
    fields = "__all__"

    widgets = {
        'model': forms.TextInput(attrs={'class': 'form-control'}),
        'color': forms.TextInput(attrs={'class': 'form-control'}),
        'model_year': forms.Textarea(attrs={'class': 'form-control'}),

    }