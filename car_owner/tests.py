import pytest
from django.core.exceptions import ValidationError
from .forms import CarAddingForm


@pytest.fixture
def valid_form_data():
    return {
        "make": "Toyota",
        "car_model": "Corolla",
        "image": None,
        "model_year": 2019,
        "color": "Red",
        "num_seats": 5,
        "plate_number": "ABC1234",
        "late_return_fee_per_hr": 5,
        "mileage": 50000,
        "fuel_type": "Gas",
        "like": False,
        "description": "",
    }


def test_car_adding_form_valid(valid_form_data):
    form = CarAddingForm(data=valid_form_data)
    assert form.is_valid()


def test_car_adding_form_invalid_plate_number():
    form_data = {
        "make": "Toyota",
        "car_model": "Corolla",
        "photo": None,
        "model_year": 2019,
        "color": "Red",
        "num_seats": 5,
        "plate_number": "ABCD1234",  # invalid plate number format
        "late_return_fee_per_hr": 5,
        "mileage": 50000,
        "fuel_type": "Gas",
        "like": False,
        "description": "",
    }
    form = CarAddingForm(data=form_data)
    with pytest.raises(ValidationError) as e:
        form.is_valid(raise_exception=True)
    assert str(e.value) == "Invalid Zimbabwean number plate"
