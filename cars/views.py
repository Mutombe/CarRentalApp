from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, SavedCars
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, ListView
from django.views.generic.edit import UpdateView, DeleteView
#from .filters import CarFilter
from .models import Like, DisLike
from .forms import CarsForm 
from django.http import JsonResponse
from django import template


def all_cars(request):
    cars = Car.objects.all()
    context = {
        'cars':cars
    }
    return render(request, 'cars/cars.html', context)
  
  
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    save_button = 0
    if SavedCars.objects.filter(user=request.user).filter(car=car).exists():
        save_button = 1
    photo = car.image
    context = {
        'car':car,
        'photo': photo
    }
    return render(request, 'cars/car_profile.html', context)

@login_required
def save_car(request, id):
    user = request.user
    car = get_object_or_404(Car, id=id)
    saved, created = SavedCars.objects.get_or_create(car=car, user=user)
    return HttpResponseRedirect('/job/{}'.format(car.id))


def saved_cars(request):
    cars = SavedCars.objects.filter(
        user=request.user).order_by('-date_posted')
    return render(request, 'cars/saved_cars.html', {'cars': cars, 'candidate_navbar': 1})


register = template.Library()
@register.simple_tag(takes_context=True)
def is_saved(context, car):
    if context['user'].is_authenticated:
        saved_car = SavedCars.objects.filter(user=context['user'], car=car).first()
        return saved_car is not None
    else:
        return False


@login_required
def save_car(request, car_id):
    if request.user.is_authenticated:
        car = get_object_or_404(Car, id=car_id)
        SavedCars.objects.create(user=request.user, car=car)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

def saved_cars(request):
    if request.user.is_authenticated:
        saved_cars = SavedCars.objects.filter(user=request.user).order_by('-saved_at')
        return render(request, 'saved_cars.html', {'saved_cars': saved_cars})
    else:
        return render(request, 'saved_cars.html', {'saved_cars': []})


@login_required
def remove_car(request, id):
    user = request.user
    car = get_object_or_404(Car, id=id)
    saved_car = SavedCars.objects.filter(car=car, user=user).first()
    saved_car.delete()
    return HttpResponseRedirect('/saved_cars/{}'.format(car.id))

def photo(request, pk):
    car = get_object_or_404(Car, pk=pk)
    context = {
        'car':car
    }
    return render(request, 'cars/photo.html', context)



def like_car(request, car_id, is_like):
    if request.user.is_authenticated:
        car = get_object_or_404(Car, id=car_id)
        like, created = CarLike.objects.get_or_create(car=car, user=request.user)
        if created:
            like.is_like = is_like
            like.save()
        elif like.is_like != is_like:
            like.is_like = is_like
            like.save()
        else:
            like.delete()
        likes = car.likes.filter(is_like=True).count()
        dislikes = car.likes.filter(is_like=False).count()
        return JsonResponse({'success': True, 'likes': likes, 'dislikes': dislikes})
    else:
        return JsonResponse({'success': False})

@login_required
class UpdateCarLikes(LoginRequiredMixin, View):
    login_url = 'logins'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        car_id = self.kwargs.get('car_id', None)
        review = self.kwargs.get('review', None) # like or dislike button clicke
        car = get_object_or_404(Car, id=car_id)
        cars = Car.objects.all()

        try:
            # If child DisLike model doesnot exit then create
            car.dis_likes
        except Car.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(car = car)

        try:
            # If child Like model doesnot exit then create
            car.likes
        except Car.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(car = car)

        if review.lower() == 'like':

            if request.user in car.likes.users.all():
                car.likes.users.remove(request.user)
            else:    
                car.likes.users.add(request.user)
                car.dis_likes.users.remove(request.user)

        elif review.lower() == 'dis_like':

            if request.user in car.dis_likes.users.all():
                car.dis_likes.users.remove(request.user)
            else:    
                car.dis_likes.users.add(request.user)
                car.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse('car_list'))
        return HttpResponseRedirect(reverse('car_list'))



class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarsForm
    template_name = '.html'

class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('dashboard')


class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('car_list')

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


@require_GET
def search_cars(request):
    search_term = request.GET.get('search')

    if search_term:
        results = Car.objects.filter(make__icontains=search_term) | Car.objects.filter(car_model__icontains=search_term) | Car.objects.filter(color__icontains=search_term)

        search_results = [
            {
                'make': car.make, 
                'car_model': car.car_model, 
                'color': car.color,
            } for car in results
        ]

        return JsonResponse(search_results, safe=False)
    else:
        return JsonResponse([], safe=False)
    
def index(request):
    return render(request, 'cars/search.html')
from django.http import JsonResponse


class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 10

    def get_queryset(self):
        location = self.request.GET.get('location')
        available = self.request.GET.get('available')
        queryset = super(CarListView, self).get_queryset()
        if location:
            queryset = queryset.filter(car_location__name=location)
        if available:
            queryset = queryset.filter(is_booked=False)
        return queryset
    
