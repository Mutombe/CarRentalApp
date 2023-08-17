from .models import Car, CarsReservationHistory
from rest_framework import serializers


class CarsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "daily_rental_price"]


class CarsReservationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarsReservationHistory
        fields = ["day1", "day2" "day3", "day4", "day5", "convert_date"]
