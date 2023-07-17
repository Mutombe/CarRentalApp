from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Car_Owners' if instance.is_car_owner else 'Customers')
        instance.groups.add(group)