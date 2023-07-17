from django.contrib import admin
from .models import Car,CarImage, CarsReservationHistory

class ImageInline(admin.TabularInline):
    model = CarImage
    extra = 0
    

class AdminCarsOverview(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('make', 'color', 'model_year', 'daily_rental_price', 'id')
    search_fields = ('make', 'color')
    ordering = ('daily_rental_price',)
    list_filter = ('make', 'color',) 


admin.site.register(Car, AdminCarsOverview)