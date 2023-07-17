from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets
from django.views.generic import \
    (DetailView,
    ListView)

from .filters import CarFilter
from .forms import CarsForm #CarsReservationHistoryForm
from .models import Car, CarsReservationHistory
from .serializers import CarsSerializer, CarsReservationHistorySerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarsSerializer

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    image = car.photo
    return render(request, 'car_detail.html', {'car': car, 'image': image})


def car_filter(request):
    car_list = Car.objects.all()
    car_filter = CarFilter(request.GET, queryset=car_list)
    return render(request, 'cars/car_filter.html', {'filter': car_filter})


def cars_lists(request):
    car = Car.objects.all()
    query =request.GET.get('q')
    if query:
        car = car.filter(
            Q(make__icontains=query) |
            Q(car_model__icontains=query) |
            Q(num_seats__icontains=query) |
            Q(daily_rental_price__icontains=query)
        )

    paginator = Paginator(car, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        car = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        car = paginator.page(paginator.num_pages)
    context = {
        'car': car,
    }
    return render(request, 'cars/cars_list.html', context)

class CarListView(ListView):
    template_name = 'cars/cars.html'
    model = Car
    context_object_name = 'cars'
    paginate_by = 3
    filterset_class = CarFilter

    def get_query(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

def car_list(request):
    pg = Paginator(Car.objects.all().order_by('model_year'), 2)
    page_number = request.GET.get('page')
    try:
        cars = pg.page(page_number)
    except EmptyPage:
        cars = pg.page(pg.num_pages)
    except PageNotAnInteger:
        cars = pg.page(1)
    return render(request, 'cars/cars.html', {'cars': cars})

#@staff_member_required
#def add_car(request):
 #   submitted = False
  #  if request.method == "POST":
   #     form = CarsForm(request.POST)
    #    if form.is_valid():
     #       form.save()
      #      return HttpResponseRedirect(redirect_to=reverse('main_app:add-car'))
    #else:
     #   form = CarsForm
      #  if 'submitted' in request.GET:
       #     submitted = True
    #return render(request, "cars/add_car.html", {'form': form, 'submitted': submitted})

#def Profile_View(request, pk):
 #   car = get_object_or_404(Car, pk=pk)
  #  rentals = Rental.objects.filter(car=car)
   # return render(request, 'car_profile.html', {'car': car, 'rentals': rentals})


#def search_car(request):
 #   if request.method == "POST":
  #      search = request.POST.get('car_search')
   #     cars = Car.objects.filter(Q(brand=search) | Q(model=search))
    #    return render(request, "cars/search_car.html", {'query': search, 'query_base': cars})
    #else:
     #   return render(request, "cars/search_car.html", {})


#@login_required(login_url='/user/login/')
#def get_reservation_view(request, cars_id, *args, **kwargs):
 #   car = Car.objects.get(pk = cars_id)
  #  if car.is_booked:
   #     return HttpResponse("Vehicle is booked")
    #form = CarsReservationHistoryForm()
    #if request.POST:
     #   form = CarsReservationHistoryForm(request.POST)
      #  if form.is_valid():
       #     form.save(commit=False)
        #    day1 = form.cleaned_data.get("day1")
         #   day2 = form.cleaned_data.get("day2")
          #  day3 = form.cleaned_data.get("day3")
           # day4 = form.cleaned_data.get("day4")
            #day5 = form.cleaned_data.get("day5")
            #form.save(commit=True)
            #return redirect("main_app:cars")
    #return render(request, "cars/reservation.html", {'cars': car, 'form': form})

#@staff_member_required
#def update_view(request, cars_id):
 #   car = Car.objects.get(pk=cars_id)
  #  form = CarsForm(request.POST or None, instance=car)
   # if form.is_valid():
    #    form.save()
     #   return redirect('main_app:cars')
    #return render(request, 'cars/cars_info_update.html', {'car': car, 'form': form})

#def create_car_view(request):
 #   if request.method == 'POST':
  #      form = CarCreationForm(request.POST, request.FILES)
   #     if form.is_valid():
    #        car = form.save(commit=False)
     #       car.Owner = request.user
      #      car.save()
       #     return redirect('car_owner_dashboard.html')
    #else:
     #   form = CarCreationForm()
    #return render(request, 'create_car.html', {'form': form})
