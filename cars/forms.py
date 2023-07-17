from django.forms import ModelForm
from .models import Car, CarsReservationHistory
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


#class CarsReservationHistoryForm(forms.ModelForm):
 #   class Meta:
  #      model = CarsReservationHistory
   #     fields =('car', 'day1', 'day2', 'day3', 'day4', 'day5')
    #    widgets = {
     #       'day1': DateInput(),
      #      'day2': DateInput(),
       #     'day3': DateInput(),
        #    'day4': DateInput(),
         #   'day5': DateInput(),
        #}

