from django.contrib import admin
from django.contrib import admin
from .models import Chauffeur


class ChauffeurOverview(admin.ModelAdmin):
    list_display = (
        "id",
        "driver",
        "first_name",
        "driver_experience",
        "phone_number",
        "email",
        "daily_fee",
    )
    search_fields = ("daily_fee",)
    ordering = ("daily_fee",)
    list_filter = (
        "id",
        "daily_fee",
    )


admin.site.register(Chauffeur, ChauffeurOverview)
