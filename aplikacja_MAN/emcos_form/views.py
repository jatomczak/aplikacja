from django.shortcuts import render
from django.http import HttpResponse
from .forms import BusForm
from .models import Bus

# Create your views here.
def home_view(request):
    form = BusForm()
    if request.method == 'POST':
        task_form = BusForm(request.POST)
        task = task_form.save(commit=False)
        return render(request, 'emcos_form_home.html', {
            'form': form,
            'task': task,
        })
    return render(request, 'emcos_form_home.html', {
        'form': form,
    })