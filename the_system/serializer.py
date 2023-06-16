from .models import Car, Rental
from rest_framework import serializers

class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'rental_price']

class RentalPrice(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['rental_date', 'return_date']