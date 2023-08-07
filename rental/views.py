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
#from paynow import Paynow
from django.http import HttpResponse



class RentalFormView(View):
    def get(self, request, pk):
        rental = Rental.objects.get(pk=pk)
        form = RentalForm()
        return render(request, 'rental/rental_form.html', {'rental': rental, 'form':form})
    

    
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

def book_car(request):
    #context = {}
    return render(request,'rental/rental_form.html')

def generate_reciept(request):
    #context = {}
    return render(request, 'rental/rental_reciept.html')

def rental_history(request):
    #context ={}
    return render(request, 'rental/rental_records.html')

