from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.views.generic import TemplateView

from .forms import AccountRegistrationForm, AccountAuthenticationForm, AccountEditForm
from .models import Account, ClientProfile

class HomePageView(TemplateView): 
    template_name = 'home.html'


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect

def signup_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authentiacted as {user.email}")
    context = {}

    if request.POST:
        account_form = AccountRegistrationForm(request.POST)
        if account_form.is_valid():
            account_form.save()
            email=account_form.cleaned_data.get('email').lower()
            raw_password = account_form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("app_main:cars")
        else:
            context['registration_form'] = account_form

    return render(request, 'user_account_templates/signup.html', context)

def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect("app_main:cars")

def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("app_main:cars")

    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination=get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('app_main:cars')
    return render(request, "user_account_templates/login.html", context)

def account_view(request, *args, **kwargs):
    context={}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
        client_details = ClientProfile.objects.get(pk = user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['email'] = account.firstname
        context['lastname'] = account.lastname
        context['hide_email'] = account.hide_email

        if client_details:
            context['user_id'] = client_details.user_id
            context['phone_number'] = client_details.phone_number
            context['address1'] = client_details.address1
            context['address2'] = client_details.address2
            context['postcode'] = client_details.postcode
            context['city'] = client_details.city
            context['country'] = client_details.country
            context['city_region'] = client_details.city_region

        is_self = True
        is_friend = True
        user = request.user
        if user.is_authenticated and user != account:
            is_self =True
        elif not user.is_authenticated:
            is_self = False

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "user_account_templates/profile.html", context)

def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("This is not your profile.")
    context = {}
    if request.POST:
        form = AccountEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save
            return redirect("account:view", user_id=account.pk)
        else:
            form = AccountEditForm(request.POST, instance=request.user,
                                   initial={
                                    "id": account.pk,
                                    "email": account.email,
                                    "firstname": account.firstname,
                                    "lastname": account.lastname,
                                    "hide_email": account.hide_email,
                                   }
            )
            context['form'] = form
    else:
        form = AccountEditForm(
            initial={
                    "id": account.pk,
                    "email": account.email,
                    "firstname": account.firstname,
                    "lastname": account.lastname,
                    "hide_email": account.hide_email,
            }
        )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY'] =settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "user_account_templates/profile_edit.html", context)
