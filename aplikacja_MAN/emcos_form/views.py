from django.shortcuts import render
from django.http import HttpResponse
from .forms import BusForm
from .models import Bus

# Create your views here.
def home_view(request):
    form = BusForm()
    if request.method == 'POST':
        task = BusForm(request.POST)
        task.save(commit=False)
        task.download_data_from_db()
        task.save()
        return render(request, 'emcos_form_home.html', {
            'form': form,
            'Bus': task,
        })
    return render(request, 'emcos_form_home.html', {
        'form': form,
    })