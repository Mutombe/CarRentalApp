import re
from django import forms
from cars.models import Car, CarImage
from django.core.exceptions import ValidationError
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField
#from django.forms import ClearableFileInput

def validate_zimbabwean_plate_number(value):
    if not re.match(r'^[A-Z]{3}\d{4}$', value):
        raise ValidationError('Invalid Zimbabwean number plate')

class CarAddingForm(forms.ModelForm):
    pass

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

class CarForm(forms.ModelForm):
    
    image = MultiImageField(
        min_num = 1,
        max_num=3,
        max_file_size=1024*1024*5,
    )
    
    class Meta:
        model = Car
        exclude = ['id', 'owner', 'is_booked', 'capacity', 'like']
        fields = ["make","car_model","daily_rental_price","late_return_fee_per_hr","plate_number","model_year", "fuel_type","color","num_seats","description"]
        
class ImageForm(forms.ModelForm):
    class Meta:
        models =CarImage
        fields = ['image']