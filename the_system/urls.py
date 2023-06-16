from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "car_rental"
urlpatterns = [
    path('', TemplateView.as_view('templates/home.html'), name='home')
    #re_path(r'^login/$', views.user_login, name='username')
]