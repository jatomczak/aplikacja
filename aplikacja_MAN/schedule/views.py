from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SelectTimeRangeForm
from . import scripts
from datetime import datetime, timedelta
from datetime import date

DATE_FORMAT = '%Y-%m-%d'


def convert_string_to_date(date:str):
    return datetime.strptime(date, DATE_FORMAT).date()

def create_date_range_list(date_from, num_days):
    date_list = []
    for i in range(0,num_days):
        date_list.append(str(date_from + timedelta(days=i)))
    return date_list


@login_required
def home_view(request):
    department_name = request.user.group.group_name
    form = SelectTimeRangeForm
    holidays_list = scripts.get_data_from_harm_for_user(department=department_name)
    if request.method == 'POST':
        date_from = convert_string_to_date(request.POST['date_from'])
        date_to = convert_string_to_date( request.POST['date_to'])
        period_length = (date_to - date_from).days + 1
        date_range_list = create_date_range_list(date_from, period_length)
        holidays_list = scripts.get_data_from_harm_for_user(
            department=department_name,
            date_from=date_from,
            date_to=date_to,
        )
        return render(request, 'home.html', {'data': holidays_list, 'form': form, 'period_length': date_range_list})
    else:
        return render(request, 'home.html', {'form': form})