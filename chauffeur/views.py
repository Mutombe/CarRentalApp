from django.shortcuts import redirect, render
from rental.models import Rental
from .models import Chauffeur
from .forms import ChauffeurForm
from django.views.generic import ListView
from django.contrib import messages


def chauffeur_add(request):
    if request.method == 'POST':
        form = ChauffeurForm(request.POST, request.FILES)
        if form.is_valid():
            chauffeur = form.save(commit=False)
            chauffeur.user = request.user
            chauffeur.save()
            messages.success(request, 'Chuffeur added successfully')
            return redirect('chauffeur_dash')
    else:
        form = ChauffeurForm()
    return render(request, 'chauffeur/chauffeur_add.html', {'form': form})

def edit_chauffeur(request, chauffeur_id):
    chauffeur = Chauffeur.objects.get(id=chauffeur_id)
    if request.method == 'POST':
        form = ChauffeurForm(request.POST, request.FILES, instance=chauffeur)
        if form.is_valid():
            form.save()
            return redirect('chauffeur_dashboard', chauffeur_id=chauffeur_id)
    else:
        form = ChauffeurForm(instance=chauffeur)
    return render(request, 'chauffeur/edit_confirm.html', {'form': form})

def chauffeur_dashboard(request):
    rentals = Rental.objects.filter(chauffeur=request.user, status='Completed').order_by('-id')
    context = {'rentals': rentals}
    return render(request, 'chauffeur/dashboard.html', context)

class ChauffeurListView(ListView):
    model = Chauffeur
    template_name = 'chauffeur/chauffeur_list.html'
    context_object_name = 'chauffeurs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(ChauffeurListView, self).get_queryset()
        first_name = self.request.GET.get('first_name')
        last_name = self.request.GET.get('last_name')
        phone_number = self.request.GET.get('phone_number')
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if phone_number:
            queryset = queryset.filter(phone_number__icontains=phone_number)
        return queryset
    
def chauffeur_reciept(request):
    #context = {}
    return render(request, 'chauffeur/chauffuer_reciept.html')

def chauffuer_rental_history(request):
    #context = {}
    return render(request, 'chauffeur/chauffeur_rental_history.html')
