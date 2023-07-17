from django.urls import path, include
from . import views  
from rest_framework import routers

router = routers.DefaultRouter()


app_name = 'main_app'

urlpatterns = [
    path('', views.CarListView.as_view(), name="cars"),
    path('car_list/', views.cars_lists, name='car_list'),
    #path('add_car/', views.add_car, name='add-car'),
    #path('search_car/', views.search_car, name='search-car'),
    path('filter_car/', views.car_filter, name='car-filter'),
    #path('cars/<cars_id>', views.get_reservation_view, name='reservation'),
    #path('update/<cars_id>', views.update_view, name='car-update'),
    #path('detail/<int:id>', views.Profile_View, name='car_profile'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
