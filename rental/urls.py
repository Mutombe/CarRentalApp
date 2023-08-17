from django.urls import path
from . import views


urlpatterns = [
    path("rental/<int:pk>/book", views.book_car, name="rental_form"),
    path("rental_history/", views.rental_history, name="rental_history"),
    path("reciept/", views.generate_reciept, name="generate_reciept"),
    path("rental/<int:pk>/", views.rental_details, name="rental_detail"),
    # path('rental_details/<int:rental_id>/', views.rental_details, name='rental_details'),
]
