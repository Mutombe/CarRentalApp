from django.urls import path
from . import views
from .views import (
    CarAddView,
    CarUpdateView,
    CarDeleteView,
)



urlpatterns = [
    path('dashboard', views.owner_page, name='dashboard'),
    path('add/', CarAddView.as_view(), name="add"),
    path('update', CarUpdateView.as_view(), name='update'),
    path('delete', CarDeleteView.as_view(), name='delete'),
]
