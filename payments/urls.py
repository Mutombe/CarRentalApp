from django.urls import path
from .views import PaynowView

urlpatterns = [
    path("paynow/<int:pk>/", PaynowView.as_view(), name="paynow"),
]
