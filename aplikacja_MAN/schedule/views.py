from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from clients.models import User
# Create your views here.

@login_required
def home_view(request):
    department = request.user.group
    user_list = User.objects.filter(group=department)
    user_id_list = []
    for user in user_list:
        user_id_list.append(user.user_id)
    return HttpResponse(user_id_list)
