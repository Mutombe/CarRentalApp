from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .forms import CreateUserForm,CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_change/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'password_change/password_reset_email.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_change/password_reset_complete.html'
    success_url = reverse_lazy('password_reset_complete')
 
def register_page(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect("logins")

        context = {"form": form}
        return render(request, "user_account_templates/register.html", context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('landingpage')
            else:
                messages.info(request, "Username or Password is incorrect")
        context = {}
        return render(request, "user_account_templates/logins.html", context)

def logout_user(request):
    logout(request)
    return redirect('logins')