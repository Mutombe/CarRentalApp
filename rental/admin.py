from django.contrib import admin
from .models import Rental, RentalHistory


class AdminRentalOverview(admin.ModelAdmin):
    list_display = (
        "id",
        "car",
        "customer",
        "status",
        "customer_destination",
        "start_date",
        "end_date",
        "with_chauffeur",
    )
    search_fields = ("car", "status")
    ordering = ("status",)
    list_filter = (
        "status",
        "start_date",
    )


admin.site.register(Rental, AdminRentalOverview)
