from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, SavedCar
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, ListView
from django.views.generic.edit import UpdateView, DeleteView

# from .filters import CarFilter
from .models import Like, DisLike
from .forms import CarsForm, SaveCarForm
from django.http import JsonResponse
from django.views.generic import TemplateView


def all_cars(request):
    cars = Car.objects.all().order_by("-created_at")
    context = {
        "cars": cars,
    }
    return render(request, "cars/cars.html", context)


@login_required
def save_car(request, pk):
    user = request.user
    car = get_object_or_404(Car, pk=pk)
    saved, created = SavedCar.objects.get_or_create(car=car, user=user)
    return HttpResponseRedirect("/car/{}".format(car.pk))


@login_required
def remove_car(request, pk):
    user = request.user
    car = Car.objects.get(pk=pk)
    saved_car = SavedCar.objects.filter(car=car, user=user).first()
    saved_car.delete()
    return HttpResponseRedirect("/car/{}".format(car.pk))


def car_detail(request, pk):
    car = Car.objects.get(pk=pk)
    save_button = 0
    if SavedCar.objects.filter(user=request.user).filter(car=car).exists():
        save_button = 1
    photo = car.image
    context = {"car": car, "photo": photo, "save_button": save_button}
    return render(request, "cars/car_profile.html", context)


def user_saved_cars(request):
    saved_cars = SavedCar.objects.filter(user=request.user).order_by("-date_saved")
    context = {"saved_cars": saved_cars}
    return render(request, "cars/saved_cars.html", context)


def photo(request, pk):
    car = get_object_or_404(Car, pk=pk)
    context = {"car": car}
    return render(request, "cars/photo.html", context)


class UpdateCarLikes(LoginRequiredMixin, TemplateView):
    template_name = "cars/cars.html"
    login_url = "logins"
    redirect_field_name = "next"

    def get(self, request, *args, **kwargs):
        car_id = self.kwargs.get("car_id", None)
        review = self.kwargs.get("review", None)  # like or dislike button clicke
        car = get_object_or_404(Car, id=car_id)

        try:
            # If child DisLike model doesnot exit then create
            car.dis_likes
        except Car.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(car=car)

        try:
            # If child Like model doesnot exit then create
            car.likes
        except Car.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(car=car)

        if review.lower() == "like":
            if request.user in car.likes.users.all():
                car.likes.users.remove(request.user)
            else:
                car.likes.users.add(request.user)
                car.dis_likes.users.remove(request.user)

        elif review.lower() == "dis_like":
            if request.user in car.dis_likes.users.all():
                car.dis_likes.users.remove(request.user)
            else:
                car.dis_likes.users.add(request.user)
                car.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse("car_list"))
        return HttpResponseRedirect(reverse("car_list"))


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy("dashboard")


class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    success_url = reverse_lazy("car_list")

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


def car_filter(request):
    car_list = Car.objects.all()
    car_filter = CarFilter(request.GET, queryset=car_list)
    car_list = car_filter.qs
    return render(request, "cars/car_filter.html", {"filter": car_filter})


def cars_lists(request):
    car = Car.objects.all()
    query = request.GET.get("q")
    if query:
        car = car.filter(
            Q(make__icontains=query)
            | Q(car_model__icontains=query)
            | Q(color__icontains=query)
            | Q(num_seats__icontains=query)
            | Q(daily_rental_price__icontains=query)
        )

    paginator = Paginator(car, 12)  # Show 15 contacts per page
    page = request.GET.get("page")
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        car = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        car = paginator.page(paginator.num_pages)
    context = {
        "car": car,
    }
    return render(request, "cars/cars_list.html", context)


@require_GET
def search_cars(request):
    search_term = request.GET.get("search")

    if search_term:
        results = (
            Car.objects.filter(make__icontains=search_term)
            | Car.objects.filter(car_model__icontains=search_term)
            | Car.objects.filter(image__icontains=search_term)
            | Car.objects.filter(color__icontains=search_term)
        )

        search_results = [
            {
                "pk": car.pk,
                "make": car.make,
                "car_model": car.car_model,
                "image": str(car.image.url),
                "color": car.color,
            }
            for car in results
        ]

        return JsonResponse(search_results, safe=False)
    else:
        return JsonResponse([], safe=False)


def index(request):
    return render(request, "cars/search.html")


class CarListView(ListView):
    model = Car
    template_name = "cars/car_list.html"
    context_object_name = "cars"
    paginate_by = 10

    def get_queryset(self):
        location = self.request.GET.get("location")
        available = self.request.GET.get("available")
        queryset = super(CarListView, self).get_queryset()
        if location:
            queryset = queryset.filter(car_location__name=location)
        if available:
            queryset = queryset.filter(is_booked=False)
        return queryset

# def Profile_View(request, pk):
#   car = get_object_or_404(Car, pk=pk)
#  rentals = Rental.objects.filter(car=car)
# return render(request, 'car_profile.html', {'car': car, 'rentals': rentals})


# def search_car(request):
#   if request.method == "POST":
#      search = request.POST.get('car_search')
#     cars = Car.objects.filter(Q(brand=search) | Q(model=search))
#    return render(request, "cars/search_car.html", {'query': search, 'query_base': cars})
# else:
#   return render(request, "cars/search_car.html", {})



