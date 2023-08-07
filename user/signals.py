from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_car_owner:
            group = Group.objects.get(name='Car_Owners')
        elif instance.is_chauffeur:
            group = Group.objects.get(name='Chauffeurs')
        else:
            group = Group.objects.get(name='Customers')
            