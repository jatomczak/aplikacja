from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import scripts

@login_required
def home_view(request):
    department_name = request.user.group.group_name
    holidays_list = scripts.get_data_from_harm_for_user(department=department_name)
    return render(request, 'home.html', {'result': holidays_list})
