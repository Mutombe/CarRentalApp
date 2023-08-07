from .models import Car, CarsReservationHistory
from rest_framework import serializers


class CarsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'daily_rental_price']

