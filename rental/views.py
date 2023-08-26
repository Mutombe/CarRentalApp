import datetime
from datetime import timedelta
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from .models import Rental, Chauffeur
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import RentalForm
from payments.models import Payment
from .models import Car, Rental, RentalHistory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .forms import RentalForm
from django.http import HttpResponse


def book_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        form = RentalForm(request.POST)
        if form.is_valid():
            booking_data = form.cleaned_data
            # store data in in a seesion
            request.session["booking_data"] = booking_data
            with_chauffeur = booking_data.get('with_chauffeur')
            if with_chauffeur:
                return redirect('choose_chauffeur_list')
            else:
                return redirect('booking_confirmation', pk=car.pk)
    else:
        form = RentalForm()
    return render(request, "rental/rental_form.html", {"car": car, "form": form})


def booking_confirmation(request, pk):
    car = get_object_or_404(Car, pk=pk)
    rental = None
    chauffeur_id = request.POST.get(Chauffeur.id)
        # Retrieve the stored booking data from the session
    booking_data = request.session.get("booking_data")
    if booking_data:
        chauffeur_present = booking_data.get("with_chauffeur")
        chauffeur = None
        if chauffeur_present:
            chauffeur = get_object_or_404(Chauffeur, id=chauffeur_id)
            booking_data["chauffeur"] = chauffeur
            price = car.ecocash_rate * (car.daily_rental_price + chauffeur.daily_fee)
        else:
            price = car.ecocash_rate * car.daily_rental_price

            # Send an email to the chauffeur
            # send_email_to_chauffeur(booking_data, car, chauffeur) 
        

        rental = Rental(
            car=car,
            customer = request.user,
            start_date=booking_data["start_date"],
            end_date=booking_data["end_date"],
            customer_destination=booking_data["customer_destination"],
            payment_method=booking_data["payment_method"],
            with_chauffeur=bool(chauffeur_id),
            rental_cost=price,
            chauffeur=chauffeur if chauffeur_present else None, 
            status = "Completed"  
        )
        rental.save()
        # Clear the booking data from the session
        del request.session["booking_data"]
        return redirect("rental_detail", pk=rental.pk)

    else:
        messages.success(request, "Just rendered your rental details")
        return render(request, "rental/booking_confirmation.html", {"car": car, "rental": rental})
   

def chauffeur_list(request):
    chauffeurs = Chauffeur.objects.all()
    context = {"chauffeurs": chauffeurs}
    return render(request, "rental/chauffeurs.html", context)

def rental_details(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    return render(request, "rental/rental_details.html", {"rental": rental})


def generate_reciept(request):
    # context = {}
    return render(request, "rental/rental_reciept.html")


def rental_history(request):
    # context ={}
    return render(request, "rental/rental_records.html")

