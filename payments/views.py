import time
from django.shortcuts import render
from django.views import View
from rental.models import Rental
from paynow import Paynow
from car_rental.settings import (
    PAYNOW_INTEGRATION_ID,
    PAYNOW_INTEGRATION_KEY,
    PAYNOW_RETURN_URL,
    PAYNOW_RESULT_URL,
)
from django.shortcuts import render, get_object_or_404


#class PaynowView(View):
#    def get(self, request, pk):
#        rental = get_object_or_404(Rental, pk=pk)
#        car = rental.car.car_model
#        identifier = rental.id
#        payer_email = rental.customer.email
#        car_owner = rental.car.owner.username
#        rental.payment_method = request.GET.get("payment_method")
#        if rental.payment_method == "Ecocash":
#            fee = rental.calculate_rental_fee()
#            try:
#                client = Paynow(
#                    PAYNOW_INTEGRATION_ID,
#                    PAYNOW_INTEGRATION_KEY,
#                    PAYNOW_RETURN_URL,
#                    PAYNOW_RESULT_URL,
#                )
#                payment = client.create_payment(identifier, payer_email)
#                payment.add(car, fee)
#                response = client.send(payment)
#                if response.success:
#                    poll_url = response.poll_url
#                    print("Poll Url: ", poll_url)
#                    status = None
#                    while status is None or status.status == "Polling":
#                        status = client.check_transaction_status(poll_url)
#                        time.sleep(5)
#                    print("Payment Status: ", status.status)
#                    if status.status == "Paid":
#                        return render(request, "payment/success_payment.html")
#                    else:
#                       raise Exception("Payment Failed")
#                else:
#                    raise Exception("Payment Failed")
#            except Exception as e:
#                return render(
#                    request, "payment/failure_payment.html", {"error": str(e)}
#                )
#        else:
#            return render(
#                request,
#                "payment/failure_payment.html",
#                {"error": "Invalid Payment Method"},
#            )
