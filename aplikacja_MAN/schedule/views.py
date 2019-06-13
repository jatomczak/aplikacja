from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_view(request):
    department = request.user.group.group_name
    return HttpResponse('Widok glowny dla dzialu %s '% department)
