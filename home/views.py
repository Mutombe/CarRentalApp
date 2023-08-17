from django.http import HttpResponse
import random
from django.shortcuts import render, redirect, get_object_or_404
from cars.models import Car
from django.contrib.auth.decorators import login_required


@login_required(login_url="logins")
def landingpage(request):
    cars = list(Car.objects.all())
    latest_car = Car.objects.latest("created_at")
    context = {"cars": cars, "latest_car": latest_car}
    return render(request, "landingpage.html", context)


def homepage_car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    display = car.get_image(0)
    return render(request, "car_detail.html", {"car": car, "display": display})
