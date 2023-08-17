import re
from django import forms
from user.models import UserProfile
from cars.models import Car
from django.core.exceptions import ValidationError

#from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField
#from django.forms import ClearableFileInput

def validate_zimbabwean_plate_number(value):
    if not re.match(r'^[A-Z]{3}\d{4}$', value):
        raise ValidationError('Invalid Zimbabwean number plate')
    
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['id', 'owner', 'is_booked', 'capacity', 'like']
        fields = ["image","make","car_model","daily_rental_price","late_return_fee_per_hr","ecocash_rate","plate_number","mileage","model_year", "fuel_type","color","num_seats","description"]
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        fields = ['profile_pic', 'phone_number', 'city', 'address']
        
        labels = {
            'profile_pic': 'Profile Picture',
            'phone_number': 'Phone Number',
            'city': 'City',
            'address': 'Address',
        }
        
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    
#class MultipleFileInput(forms.ClearableFileInput):
#   allow_multiple_selected = True
    
#class MultipleFileField(forms.FileField):
#    def __init__(self, *args, **kwargs):
#        kwargs.setdefault("widget", MultipleFileInput())
#        super().__init__(*args, **kwargs)
        
#    def clean(self, data, initial=None):
#        single_file_clean = super().clean
#        if isinstance(data, (list, tuple)):
#            result = [single_file_clean(d, initial) for d in data]
#        else:
#            result = single_file_clean(data, initial)
#            return result


        
