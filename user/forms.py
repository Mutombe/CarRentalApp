from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser
from django import forms 


class CreateUserForm(UserCreationForm):
    is_car_owner = forms.BooleanField(required=False, label='Are you a car owner ?')
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'is_car_owner']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_car_owner = self.cleaned_data.get('is_car_owner', False)
        if commit:
            user.save()
        return user

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'autocomplete': 'email', 'class': 'form-control'}
        ))