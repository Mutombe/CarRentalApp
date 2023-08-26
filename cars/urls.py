from django.urls import path, include
from .views import UpdateCarLikes
from . import views

urlpatterns = [
    path("car_list/", views.all_cars, name="car_list"),
    path("car/<int:pk>/", views.car_detail, name="car_detail"),
    path("photo/<int:pk>/", views.photo, name="photo"),
    path("car/<int:pk>/save/", views.save_car, name="save-car"),
    path("saved_car_list/", views.user_saved_cars, name="saved-cars"),
    path("car/<int:pk>/remove/", views.remove_car, name="remove-car"),
    path(
        "car_review/<int:car_id>/<str:review>",
        UpdateCarLikes.as_view(),
        name="car_review",
    ),
    path("car/<int:car_id>/remove/", views.remove_car, name="remove_from_saved"),
    path("index/", views.index, name="index"),
    path("search_cars/", views.search_cars, name="search_cars"),
    path("filter_car/", views.car_filter, name="car-filter"),
]
