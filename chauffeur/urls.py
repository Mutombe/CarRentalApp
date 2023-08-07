from  django.urls import path
from . import views


urlpatterns = [
    path('add_chauffeur', views.chauffeur_add, name='add_chauffeur'),
    path('chauffeur_dashboard', views.chauffeur_dashboard, name='chauffeur_dashboard'),
    path('edit_chauffeur', views.edit_chauffeur, name='edit_chauffeur'),
    path('chauffeur_rental_history', views.chauffuer_rental_history, name='chauffeur_rental_history'),
    path('chauffeur_reciept', views.chauffeur_reciept, name='chauffeur_reciept'),
    path('chauffeurs/', views.ChauffeurListView.as_view(), name='chauffeur_list'),
]
