from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register_page, name="register"),
    path("logins/", views.login_page, name="logins"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile, name="profile"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="user_account_templates/password_reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="user_account_templates/password_reset_sent.html"
        ),
        name="password_reset_sent",
    ),
    path(
        "reset<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user_account_templates/password_reset_form.html"
        ),
        name="reset_password_complete",
    ),
]
