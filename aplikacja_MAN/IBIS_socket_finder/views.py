from django.shortcuts import render
from django.http import HttpResponse
from .forms import BusNameForms
from . import scripts

# Create your views here.
def home_view(request):
    form = BusNameForms()
    if request.method == 'POST':
        form = BusNameForms(request.POST)
        if form.is_valid():
            fahrgnr = form.cleaned_data
            scripts.main(fahrgnr['name'])
        pass
    return render(request, 'home_page.html', {
        'form': form})
