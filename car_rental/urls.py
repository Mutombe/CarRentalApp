from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView

from user.views import(
    login_page,
    register_page,
    logout_user,
    CustomPasswordResetView, 
    CustomPasswordResetConfirmView
)

from car_owner.views import(
     owner_page,
     UploadView,
     CarUpdateView,
     CarDeleteView,
)
from the_system.views import (
    landingpage
)

app_name = 'main_app'
urlpatterns = [
     path('', landingpage, name='landingpage'),
     #path('dashboard', owner_page, name='dashboard'),
     path('logins/', login_page, name='logins'),
     path('logout/', logout_user, name="logout"),
     path('register/', register_page, name='register'),
     path('cars/', include("cars.urls")),
     #path('add/', CarAddView.as_view(), name="add"),
     path('dashboard/', UploadView.as_view(), name="dashboard"),
     path('update', CarUpdateView.as_view(), name='update'),
     path('delete', CarDeleteView.as_view(), name='delete'),
     path('contact/', include("contact.urls")),
     path('admin/', admin.site.urls),
     path('api-auth/', include('rest_framework.urls')),
     path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
     path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
     path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)