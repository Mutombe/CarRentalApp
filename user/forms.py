from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser, UserProfile
from django import forms


class CreateUserForm(UserCreationForm):
    is_car_owner = forms.BooleanField(required=False, label="Are you a car owner ?")
    is_chauffeur = forms.BooleanField(required=False, label="Are you a driver")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "is_car_owner"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_car_owner = self.cleaned_data.get("is_car_owner", False)
        user.is_car_owner = self.cleaned_data.get("is_chauffeur", False)
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["user"]
        fields = ["profile_pic", "phone_number", "city", "address"]
