from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import SelectTimeRangeForm, UploadFileForm
from .models import VacationsList
from . import scripts
from datetime import datetime, timedelta

from .scripts import handle_uploaded_file

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
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def upload_schedule(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('schedule:schedule_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload_schedule.html',{
        'form': form,
    })


def schedule_list(request):
    vacations_list_all = VacationsList.objects.filter(owner=request.user)
    if request.method == 'POST':
        if len(request.POST) == 3:
            all_arguments = list(request.POST)
            first_list = all_arguments[1]
            second_list = all_arguments[2]
            return redirect('schedule:schedules_compare', first_list=first_list, second_list=second_list)
        else:
            return render(request, 'schedule_list.html', {
                'all_lists': vacations_list_all,
                'message': 'Wybierz dokładnie dwie listy'})
    return render(request, 'schedule_list.html', {'all_lists': vacations_list_all})


def schedules_compare(request, first_list, second_list):
    first_list = VacationsList.objects.get(owner=request.user, name=first_list)
    second_list = VacationsList.objects.get(owner=request.user, name=second_list)
    return render(request, 'compare_schedules.html', {
        'first_list': first_list,
        'second_list': second_list,
    })