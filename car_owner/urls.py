from django.urls import path
from .views import CarUpdateView 
from . import views


urlpatterns = [
    path("dash/", views.dashboard, name="dash"),
    path("car_add/", views.car_add, name="car_add"),
    path("profile/add/", views.add_profile, name="add_profile"),
    path("cars/<int:pk>", views.delete_car, name="delete_car"),
    path("edit/<int:pk>", CarUpdateView.as_view()),
]
