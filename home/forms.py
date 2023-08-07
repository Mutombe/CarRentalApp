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
    
    paynow = Paynow(
    'INTEGRATION_ID', 
    'INTEGRATION_KEY',
    'http://example.com/gateways/paynow/update', 
    'http://example.com/return?gateway=paynow'
)

# Create new payment and pass in the reference and payer's email address
payment = paynow.create_payment('Order #100', 'test@example.com')

# Passing in the name of the item and the price of the item
payment.add('Bananas', 2.50)
payment.add('Apples', 3.40)

# Save the response from paynow in a variable
response = paynow.send(payment)

if response.success:

    # Get the link to redirect the user to, then use it as you see fit
    link = response.redirect_url

    # Get the poll url (used to check the status of a transaction). 
    # You might want to save this in your DB
    pollUrl = response.poll_url