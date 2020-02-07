from django.shortcuts import render
from django.http import HttpResponse
from .forms import BusForm

# Create your views here.
def home_view(request):
    form = BusForm()
    return render(request, 'emcos_form_home.html', {
        'form': form,
    })