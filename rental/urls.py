from django.urls import path
from . import views


urlpatterns = [
    path('booking/<int:pk>/', views.book_car, name='booking_form'),
    path('booking/<int:pk>/confirm/', views.booking_confirmation, name='booking_confirmation'),
    path('booking_form/chauffeurs/', views.chauffeur_list, name='choose_chauffeur_list'),
    path("rental/<int:pk>/", views.rental_details, name="rental_detail"),
    path("rental_history/", views.rental_history, name="rental_history"),
    path("reciept/", views.generate_reciept, name="generate_reciept"),
]
