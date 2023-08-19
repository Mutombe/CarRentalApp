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
            form_data = form.cleaned_data
            # store data in in a seesion
            request.session["booking_data"] = {
                "start_date": form_data["start_date"],
                "end_date": form_data["end_date"],
                "with_chauffeur": form_data["with_chauffeur"],
                "customer_destination": form_data["customer_destination"],
                "payment_method": form_data["payment_method"],
            }
            with_chauffeur = form_data.get('with_chauffeur')
            if with_chauffeur:
                return redirect('choose_chauffeur_list')
            else:
                return redirect('booking_confirmation', pk=car.pk)
    else:
        form = RentalForm()
    return render(request, "rental/rental_form.html", {"car": car, "form": form})


def booking_confirmation(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        chauffeur_id = request.POST.get(Chauffeur.id)
        chauffeur = get_object_or_404(Chauffeur, id=chauffeur_id)
        # Retrieve the stored booking data from the session
        booking_data = request.session.get("booking_data")

        if booking_data is not None:
            # Update the booking data with chauffeur selection
            booking_data["with_chauffeur"] = True
            booking_data["chauffeur"] = chauffeur.id

            # Send an email to the chauffeur
            # send_email_to_chauffeur(booking_data, car, chauffeur)

            return render(
                request,
                "rental/booking_confirmation.html",
                {"car": car, "booking_data": booking_data},
            )
    messages.success(request, "Couldn't render your rental details")
    return redirect("booking_form", pk=car.pk)

def chauffeur_list(request):
    chauffeurs = Chauffeur.objects.all()
    context = {"chauffeurs": chauffeurs}
    return render(request, "rental/chauffeurs.html", context)

def rental_details(request, pk):
    rental = get_object_or_404(Rental, pk=rental.id)
    return render(request, "rental_details.html", {"rental": rental})


def generate_reciept(request):
    # context = {}
    return render(request, "rental/rental_reciept.html")


def rental_history(request):
    # context ={}
    return render(request, "rental/rental_records.html")

