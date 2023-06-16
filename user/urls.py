from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path('<user_id>/', views.account_view, name="profile.html"),
    path('<user_id>/edit', views.edit_account_view, name="edit"),
]