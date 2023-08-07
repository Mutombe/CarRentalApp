from django.contrib import admin
from .models import CustomUser, UserProfile



class UserOverview(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_car_owner')
    search_fields = ('username', 'email')  # set search_fields to a tuple of valid fields
    
    def get_password1(self, obj):
        return "********"  # replace with a function that retrieves the user's password1
    
    def get_password2(self, obj):
        return "********"  # replace with a function that retrieves the user's password2
    
    list_display_links = ('id', 'username')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('-date_joined',)

admin.site.register(CustomUser, UserOverview)

class ProfileOverview(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_pic', 'phone_number', 'city', 'address')
    search_fields = ('city', 'address')  # set search_fields to a tuple of valid fields

admin.site.register(UserProfile, ProfileOverview)
