from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import SelectTimeRangeForm
from . import scripts
from datetime import datetime, timedelta


def create_date_range_list(date_from, num_days):
    date_list = []
    for i in range(0,num_days):
        date_list.append(str(date_from + timedelta(days=i)))
    return date_list


@login_required
def home_view(request):
    form = SelectTimeRangeForm()
    if request.method == 'POST':
        form = SelectTimeRangeForm(request.POST)
        if form.is_valid():
            department_name = request.user.group.group_name
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
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
    else:
        return render(request, 'home.html', {'form': form})


@login_required
def upload(request):
    csv_to_db = scripts.CsvToDb()
    user = request.user
    csv_to_db.import_task(user)
    return HttpResponse('test')