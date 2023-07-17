from django.urls import path
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('logins/', views.login_page, name='logins'),
    path('logout/', views.logout_user, name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
