from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .models import UserProfile
from .forms import CreateUserForm, ProfileForm


def register_page(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account was created for " + user)
                return redirect("logins")

        context = {"form": form}
        return render(request, "user_account_templates/register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("landingpage")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("landingpage")
            else:
                messages.info(request, "Username or Password is incorrect")
        context = {}
        return render(request, "user_account_templates/logins.html", context)

def logout_user(request):
    logout(request)
    return redirect("logins")

def profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    context = {
        "profile": profile,
    }
    return render(request, "user_account_templates/profile.html", context)

@login_required
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "user_account_templates/edit_profile.html", {"form": form})
