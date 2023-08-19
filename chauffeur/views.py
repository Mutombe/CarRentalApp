from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from cars.models import Car
from rental.models import Rental
from .models import Chauffeur
from .forms import ChauffeurForm
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView


def chauffeur_add(request):
    if request.method == "POST":
        form = ChauffeurForm(request.POST, request.FILES)
        if form.is_valid():
            chauffeur = form.save(commit=False)
            chauffeur.driver = request.user
            chauffeur.save()
            messages.success("Chauffeur added successfully")
            return redirect("chauffeur_dashboard")
    else:
        form = ChauffeurForm()
    return render(request, "chauffeur/chauffeur_add.html", {"form": form})


class ChauffeurUpdateView(LoginRequiredMixin, UpdateView):
    model = Chauffeur
    form_class = ChauffeurForm
    template_name = "chauffeur/edit_chauffeur.html"
    success_url = reverse_lazy("profile")


def chauffeur_list(request):
    chauffeurs = Chauffeur.objects.all()
    context = {"chauffeurs": chauffeurs}
    return render(request, "chauffeur/chauffeurs.html", context)


def chauffeur_reciept(request):
    # context = {}
    return render(request, "chauffeur/chauffuer_reciept.html")


def chauffuer_rental_history(request):
    # context = {}
    return render(request, "chauffeur/chauffeur_rental_history.html")
