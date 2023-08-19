from django import forms
from django.utils import timezone
from .models import Rental


class RentalForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    payment_method = forms.ChoiceField(
        choices=[("USD", "USD"), ("Ecocash", "Ecocash")], widget=forms.RadioSelect
    )
    customer_destination = forms.CharField(max_length=100, required=True)
    with_chauffeur = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        if start_date:
            cleaned_data['start_date'] = start_date.replace(tzinfo=None).isoformat()

        end_date = cleaned_data.get('end_date')
        if end_date:
            cleaned_data['end_date'] = end_date.replace(tzinfo=None).isoformat()

        return cleaned_data

    class Meta:
        model = Rental
        fields = [
            "start_date",
            "end_date",
            "with_chauffeur",
            "customer_destination",
            "payment_method",
        ]
