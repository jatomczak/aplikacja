from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SelectTimeRangeForm
from . import scripts
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'


def convert_string_to_date(date:str):
    return datetime.strptime(date, DATE_FORMAT).date()


@login_required
def home_view(request):
    department_name = request.user.group.group_name
    form = SelectTimeRangeForm
    holidays_list = scripts.get_data_from_harm_for_user(department=department_name)
    if request.method == 'POST':
        date_from = convert_string_to_date(request.POST['date_from'])
        date_to = convert_string_to_date( request.POST['date_to'])
        holidays_list = scripts.get_data_from_harm_for_user(
            department=department_name,
            date_from=date_from,
            date_to=date_to,
        )
    return render(request, 'home.html', {'result': holidays_list, 'form': form})
