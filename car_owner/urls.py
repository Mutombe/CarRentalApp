from django.urls import path
from .views import CarUpdateView  # , ProfileUpdateView
from . import views


urlpatterns = [
    path("dash/", views.dashboard, name="dash"),
    path("car_add/", views.car_add, name="car_add"),
    path("profile/", views.profile, name="profile"),
    path("profile/add/", views.add_profile, name="add_profile"),
    path("cars/<int:pk>", views.delete_car, name="delete_car"),
    path("edit/<int:pk>", CarUpdateView.as_view()),
    # path('edit/<int:pk>',ProfileUpdateView.as_view()),
    path("profile/edit/", views.owner_edit_profile, name="profile_edit"),
]
