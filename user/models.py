from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

class CustomUser(AbstractUser): 
    is_car_owner = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, 
                                              blank=True, 
                                              related_name='custom_user_permissions', 
                                              help_text=_('Specific permissions for the user.'), 
                                              verbose_name=_('user permissions'))

car_owner_group, created = Group.objects.get_or_create(name='Car_Owners')
customer_group, created = Group.objects.get_or_create(name='Customers')

#class UserProfile(models.Model):
    #user = models.OneToOneField(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    #phone_number = models.CharField(max_length=20, blank=True)
    #address1 = models.CharField(max_length=50, blank=True)
    #address2 = models.CharField(max_length=30, blank=True)
    #postcode = models.CharField(max_length=10, blank=True)
    #city = models.CharField(max_length=30, blank=True)
    #country = models.CharField(max_length=20, blank=True)
    #city_region = models.CharField(max_length=30, blank=True)

