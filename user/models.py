from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

class CustomUser(AbstractUser): 
    is_car_owner = models.BooleanField(default=False)
    is_chauffeur = models.BooleanField(default=False) 
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, 
                                              blank=True, 
                                              related_name='custom_user_permissions', 
                                              help_text=_('Specific permissions for the user.'), 
                                              verbose_name=_('user permissions'))

car_owner_group, created = Group.objects.get_or_create(name='Car_Owners')
car_owner_group, created = Group.objects.get_or_create(name='Chauffeurs')
customer_group, created = Group.objects.get_or_create(name='Customers')

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to="static/media/user_prof_pic/")
    phone_number = models.CharField(max_length=20, default='+263')
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user.username


