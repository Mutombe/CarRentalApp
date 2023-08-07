from django.urls import path, include
from .views import UpdateCarLikes
from . import views  

urlpatterns = [
    path('car_list/', views.all_cars, name='car_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('photo/<int:pk>/', views.photo, name='photo'),
    path('save_car/<int:car_id>/', views.save_car, name='save_car'),
    path('saved_cars/', views.saved_cars, name='saved_cars'),
    path('reviews/<int:car_id>/<str:review>', UpdateCarLikes, name='car_review'),
    path('car/<id>/remove/', views.remove_car, name='remove_from_saved'),
    path('index/', views.index, name='index'),
    path('search_cars/', views.search_cars, name='search_cars'),
    path('filter_car/', views.car_filter, name='car-filter'),
    path('search/', views.search_page, name='search'),

]

    
