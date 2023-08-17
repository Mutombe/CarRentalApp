from django import forms
from .models import Chauffeur


class ChauffeurForm(forms.ModelForm):
    class Meta:
        model = Chauffeur
        fields = [
            "profile_photo",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "driver_experience",
            "ecocash_rate",
            "daily_fee",
        ]
