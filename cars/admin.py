from django.contrib import admin
from .models import Car

class AdminCarsOverview(admin.ModelAdmin):
    list_display = ('id','image','make', 'color', 'owner', 'model_year', 'daily_rental_price', )
    search_fields = ('make', 'color')
    ordering = ('daily_rental_price',)
    list_filter = ('make', 'color',) 


admin.site.register(Car, AdminCarsOverview)