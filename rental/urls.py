from  django.urls import path
from . import views


urlpatterns = [
    path('rental_history/', views.rental_history, name='rental_history'),
    path('reciept/', views.generate_reciept, name='generate_reciept'),
    path('rental-form/<int:pk>/', views.RentalFormView.as_view(), name='rental_form'),
    path('rental/<int:pk>/', views.RentalDetailView.as_view(), name='rental_detail'),
    #path('rental_details/<int:rental_id>/', views.rental_details, name='rental_details'),
]