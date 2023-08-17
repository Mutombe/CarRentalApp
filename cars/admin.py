from django.contrib import admin
from .models import Car, SavedCar, DisLike, Like


class AdminCarsOverview(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
        "make",
        "color",
        "owner",
        "model_year",
        "daily_rental_price",
    )
    search_fields = ("make", "color")
    ordering = ("daily_rental_price",)
    list_filter = (
        "make",
        "color",
    )


class AdminSavedCarsOverview(admin.ModelAdmin):
    list_display = (
        "user",
        "car",
        "date_saved",
    )
    search_fields = ("user",)
    ordering = ("user",)
    list_filter = ("car",)


class AdminLikedCarsOverview(admin.ModelAdmin):
    list_display = ("car", "created_at", "updated_at")
    search_fields = ("users",)
    ordering = ("users",)
    list_filter = ("car",)


class AdminDislikedCarsOverview(admin.ModelAdmin):
    list_display = ("car", "created_at", "updated_at")
    search_fields = ("users",)
    ordering = ("users",)
    list_filter = ("car",)


admin.site.register(SavedCar, AdminSavedCarsOverview)
admin.site.register(Car, AdminCarsOverview)
admin.site.register(Like, AdminLikedCarsOverview)
admin.site.register(DisLike, AdminDislikedCarsOverview)
