from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from cars.models import Car, CarImage
from django.views.generic.edit import FormView
from .forms import CarForm,CarAddingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
import os


@login_required
def owner_page(request):
    cars = Car.objects.filter(owner=request.user)
    context={
        'cars':cars
    }
    return render(request, 'car_owner/dashboard.html', context)

class UploadView(FormView):
    form_class = CarForm
    template_name = 'car_owner/dashboard.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        car = form.save(commit=False)
        car.owner = self.request.user
        car.save()
        
        for image_file in self.request.FILES.getlist('image'):
            ext = os.path.splittext(image_file.name)[1]
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            if ext.lower() not in allowed_extensions:
                raise ValidationError("File type not supported.")
            CarImage.objects.create(car=car, image=image_file)
        return super().form_valid(form)
    

             

@login_required
def view_car(request, pk):
    cars = Car.objects.get(pk=pk, owner=request.user)
    photos = cars.images.all()
    context = {
        'car': cars,
        'photos': photos
    }
    return render(request, 'car_owner/dashboard.html', context)

class CarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model =Car
    form_class = CarAddingForm
    template_name = 'car_owner/create_car.html'
    success_url = reverse_lazy('dashboard')
    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner

class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    template_name = 'car_owner/confirm.html'
    success_url = reverse_lazy('dashboard')
    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


