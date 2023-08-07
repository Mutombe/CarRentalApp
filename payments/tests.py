from django.test import TestCase
from django.urls import reverse
from .models import Payment
import pytest

@pytest.mark.django_db
def test_paynow_notification(client):
    # Create a payment to test with
    payment = Payment.objects.create(
        reference='12345678',
        customer='test@gmail.com',
        fee=10000.0,
        status='',
        transaction_id='4',
    )

    url = reverse('paynow-notify')
    data = {
        'reference': '12345678',
        'status': 'Paid',
        'polling_id': '1234',
    }
    response = client.post(url, data)

    assert response.status_code == 200

    # Refresh the payment object from the database and assert that its status has been updated
    payment.refresh_from_db()
    assert payment.status == 'Paid'
    assert payment.transaction_id == '1234'
# Create your tests here.
