from django.urls import path
from .views import ChauffeurUpdateView
from . import views


urlpatterns = [
    path("add_chauffeur", views.chauffeur_add, name="add_chauffeur"),
    path("chauffeur_list", views.chauffeur_list, name="chauffeur_list"),
    path(
        "chauffeur_rental_history",
        views.chauffuer_rental_history,
        name="chauffeur_rental_history",
    ),
    path("chauffeur_reciept", views.chauffeur_reciept, name="chauffeur_reciept"),
    path(
        "chauffeur_edit/<int:pk>/", ChauffeurUpdateView.as_view(), name="chauffeur_edit"
    ),
]
