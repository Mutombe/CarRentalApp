from django.test import TestCase
import pytest
from django.urls import reverse
from user.models import CustomUser
from .models import Car, Like, DisLike

@pytest.fixture
def car():
    car = Car.objects.create(make="Toyota", car_model="Jaino", city="Harare", residence="Budiriro", model_year="2013", color="Blue", num_seats="4", plate_number="AGC2322", is_booked=True)
    return car

@pytest.fixture
def user():
    user = CustomUser.objects.create(username="testuser", email="test@gmail.com", password="testpassword")
    return user

@pytest.mark.django_db
def test_like_car(client, car, user):
    client.login(username="testuser", password="testpassword")

    response = client.post(
        reverse("car_like", kwargs={"car_id": car.id, "review": "like"})
    )

    assert response.status_code == 200
    assert car.likes.users.filter(id=user.id).exists()
    assert not car.dis_likes.users.filter(id=user.id).exists()