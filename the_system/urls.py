from django.urls import path
from django.views.generic import TemplateView
from .views import homepage_car_detail

app_name = "car_rental"
urlpatterns = [
    path('', TemplateView.as_view('landingpage.html'), name='landing'),
    path('cars/<int:pk>/', homepage_car_detail, name='home_car_details'),
    #re_path(r'^login/$', views.user_login, name='username')
]