import datetime
from datetime import timedelta
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from .models import Rental, Chauffeur
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import RentalForm
from payments.models import Payment
from .models import Car, Rental, RentalHistory 
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from .forms import RentalForm
#from paynow import Paynow
from django.http import HttpResponse

def book_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    customer = request.user 
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.status = "In Progress"
            rental.car = car
            rental.customer = customer
            rental.save()
            rental.status = "Completed"
            return redirect('rental_detail')
    else:
        form = RentalForm()
    context = {
        'form': form,
        'car': car,
        'customer': customer,
    }
    return render(request, 'rental/rental_form.html', context)

def rental_details(request, pk):
    rental = get_object_or_404(Rental, pk=rental.id)
    return render(request, 'rental_details.html', {'rental': rental})

    
def generate_reciept(request):
    #context = {}
    return render(request, 'rental/rental_reciept.html')

def rental_history(request):
    #context ={}
    return render(request, 'rental/rental_records.html')

class RentalCreateView(LoginRequiredMixin, CreateView):
    model = Rental
    form_class = RentalForm
    template_name = 'rentals/rental_form.html'

    def get_context_data(self, **kwargs):
        context = super(RentalCreateView, self).get_context_data(**kwargs)
        context['car'] = Car.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        rental = form.save(commit=False)
        rental.car = Car.objects.get(pk=self.kwargs['pk'])
        rental.customer = self.request.user
        rental.daily_rental_price = rental.car.daily_rental_price
        rental.late_return_fee = rental.car.late_return_fee_per_hr
        rental.ecocash = self.request.POST.get('payment_method') == 'Ecocash'
        if rental.start_date > rental.end_date:
            form.add_error('start_date', 'Start date cannot be after end date')
            return self.form_invalid(form)
        if rental.ecocash and not rental.car.ecocash_rate:
            form.add_error('payment_method', 'Ecocash is not available for this car')
            return self.form_invalid(form)
        rental.save()
        return super(RentalCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('rental_detail', kwargs={'pk': self.object.pk})
    
class RentalDetailView(LoginRequiredMixin, DetailView):
    model = Rental
    template_name = 'rentals/rental_detail.html'
    context_object_name = 'rental'

    def get_context_data(self, **kwargs):
        context = super(RentalDetailView, self).get_context_data(**kwargs)
        context['payment'] = Payment.objects.filter(rental=self.object).first()
        return context

    def post(self, request, *args, **kwargs):
        payment_method = request.POST.get('payment_method')
        rental = self.get_object()
        payment = Payment.objects.filter(rental=rental).first()
        if not payment:
            payment = Payment(rental=rental)
        payment.payment_stage = 'In Progress'
        payment.amount = rental.calculate_grand_total(payment_method)
        payment.ecocash = payment_method == 'Ecocash'
        payment.usd = payment_method == 'USD'
        payment.save()
        rental.status = 'Completed'
        rental.save()
        return HttpResponseRedirect(reverse('rental_detail', kwargs={'pk': rental.pk}))
    
class RentalCreateView(CreateView):
    model = Rental
    form_class = RentalForm
    template_name = 'rentals/rental_create.html'


    def get(self, request, *args, **kwargs):
        car_pk = self.kwargs.get('pk')
        car = get_object_or_404(Car, pk=car_pk)
        form = self.form_class(initial={'start_date': datetime.now(), 'end_date': datetime.now() + timedelta(hours=1)})
        return render(request, self.template_name, {'form': form, 'car': car})

    def form_valid(self, form):
        car_pk = self.kwargs.get('pk')
        car = get_object_or_404(Car, pk=car_pk)
        rental = form.save(commit=False)
        rental.car = car
        rental.total_cost = rental.calculate_rental_fee()
        rental.save()
        if form.cleaned_data['with_chauffeur']:
            chauffeur_pk = self.request.GET.get('chauffeur')
            chauffeur = get_object_or_404(Chauffeur, pk=chauffeur_pk)
            rental.chauffeur = chauffeur
            rental.save()
        rental_history = RentalHistory(
            rental = rental.id,
            car_owner = rental.car.owner,
            car = rental.car,
            rental_days = (rental.end_date - rental.start_date).days,
            rental_price = rental.total_cost,
            customer = rental.customer,
            customer_destination = rental.customer_destination,  
        )
        payment = Payment(rental=rental, amount=rental.total_cost)
        payment.save()
        rental_history.save()
        return redirect('rental_detail', pk=rental.pk)



def payment_create(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    payment = Payment(rental=rental, amount=rental.total_cost)

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST, instance=payment)
        if payment_form.is_valid():
            payment = payment_form.save()

            # Create a Paynow payment
            paynow = Paynow(
                settings.PAYNOW_INTEGRATION_ID,
                settings.PAYNOW_INTEGRATION_KEY,
                'https://www.paynow.co.zw/Interface/CheckOut'
            )

            result = paynow.create_payment(
                payment.reference,
                payment.customer.email,
                payment.amount,
                rental.car.make + ' rental payment',
                settings.PAYNOW_RETURN_URL,
                settings.PAYNOW_RESULT_URL
            )

            if result.success:
                # Redirect the customer to the Paynow payment page
                return HttpResponseRedirect(result.redirect_url)
            else:
                # Handle payment creation errors
                messages.error(request, 'Failed to create payment. Please try again later.')
    else:
        payment_form = PaymentForm(instance=payment)

    return render(request, 'rental/payment_create.html', {
        'rental': rental,
        'payment_form': payment_form
    })

#When a customer completes a payment on the Paynow payment page,
# Paynow will send a notification to a URL specified in your Paynow account settings.


def payment_notify(request):
    if request.method == 'POST':
        paynow = Paynow(
            settings.PAYNOW_INTEGRATION_ID,
            settings.PAYNOW_INTEGRATION_KEY,
            'https://www.paynow.co.zw/Interface/CheckOut'
        )

        result = paynow.parse_notification(request.body.decode())

        if result:
            payment = Payment.objects.get(reference=result.reference)
            payment.status = result.status
            payment.paynow_reference = result.poll_url
            payment.save()

        return HttpResponse('OK')

    return HttpResponseNotAllowed(['POST'])

@login_required

def book_rental(request, car_id):
    car = Car.objects.get(id=car_id)
    if not car.is_booked:
        messages.error(request, 'This car is not available for rental.')
        return redirect('search_cars')
    if request.method == 'POST':
        start_date = (request.POST.get('start_date'))
        end_date = (request.POST.get('end_date'))
        total_price = request.POST.get('total_price')
        payment_status = request.POST.get('payment_status')
        rental = Rental.objects.create(
            customer=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            payment_status=payment_status
        )
        car.is_booked = False
        car.save()
        messages.success(request, 'Rental booked successfully.')
        return redirect('rental_detail', rental.id)
    return render(request, 'rental/rental_form.html', {'car': car})

