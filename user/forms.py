from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account, ClientProfile

class AccountRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True, help_text='Required')
    firstname = forms.CharField(max_length=60)
    lastname = forms.CharField(max_length=60)

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ('email', 'firstname', 'lastname', 'password1', 'password2')

    def clean_email_account(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model =Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Account, check your email or password")

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'firstname', 'lastname', 'hide_email' )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('"%s" is already in use.' % account)

    def save(self, commit=True):
        account = super(AccountEditForm, self).save(commit=False)
        account.email = self.cleaned_data['email'].lower()
        account.firstname = self.cleaned_data['firstname']
        account.lastname = self.cleaned_data['lastname']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account