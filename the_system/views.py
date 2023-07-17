from django.http import HttpResponse
from django.shortcuts import render,  redirect, get_object_or_404
from cars.models import Car
from django.contrib.auth.decorators import login_required

@login_required(login_url='logins')
def homepage(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': cars})

def landingpage(request):
    return render(request, 'landingpage.html')

def homepage_car_detail(request, car_id):
        car = get_object_or_404(Car, id=car_id)
        display = car.get_image(0)
        return render(request, 'car_detail.html', {'car': car, 'display': display})
