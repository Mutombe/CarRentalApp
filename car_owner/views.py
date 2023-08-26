from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from cars.models import Car
from chauffeur.models import Chauffeur
from .forms import CarForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from user.models import UserProfile
from django.contrib import messages


def car_add(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, "Car added successfully")
            return redirect("dash")
    else:
        form = CarForm()
    return render(request, "car_owner/car_add.html", {"form": form})


@login_required
def delete_car(request, pk):
    car = Car.objects.get(pk=car.pk, owner=request.user)
    if request.method == "POST":
        car.delete()
    return redirect("dash")


def dashboard(request):
    cars = Car.objects.filter(owner=request.user)
    # rentals = Rental.objects.filter(car__in=cars).order_by('-id')
    context = {"cars": cars}
    return render(request, "car_owner/dashboard.html", context)


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = "car_owner/car_update.html"
    success_url = reverse_lazy("dash")



# Multi image approach

# class UploadView(FormView):
#   form_class = CarForm
#  template_name = 'car_owner/dashboard.html'
# success_url = reverse_lazy('dashboard')

# def form_valid(self, form):
#    car = form.save(commit=False)
#   car.owner = self.request.user
#  car.save()

# image_files = self.request.FILES.getlist('image')
# if isinstance(image_files, list):
#   for image_file in image_files:
#      ext = os.path.splitext(image_files.name)[1]
#     allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
#    if ext.lower() not in allowed_extensions:
#       raise ValidationError("File type not supported.")
#  CarImage.objects.create(car=car, image=image_file)
# else:
#   image_file = image_files
#  ext = os.path.splitext(image_file)[1]
# allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
# if ext.lower() not in allowed_extensions:
#   raise ValidationError("File type not supported.")
# CarImage.objects.create(car=car, image=image_file)
# context = self.get_context_data()
# context['car'] = car

# return super().form_valid(form)
