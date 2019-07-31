from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import SelectTimeRangeForm, UploadFileForm, CompareVacationsListForm
from .models import VacationsList, VacationDetails
from . import scripts
from datetime import datetime, timedelta
import csv

from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)

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
            department_name = request.user.get_group_name()
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
        vacations_list = form.create_upload_file_form(request.user)
        if form.is_valid():
            with open(vacations_list.file.path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                for user_name, vacation_date, hours,  unique_id in csv_reader:
                    VacationDetails.create_vacation_detalis(vacation_date, hours, user_name, unique_id, vacations_list)
                return redirect('schedule:schedule_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload_schedule.html', {
        'form': form,
    })


def schedule_list(request):
    form = CompareVacationsListForm(owner=request.user)
    vacations_list_all = VacationsList.objects.filter(owner=request.user)
    return render(request, 'schedule_list.html', {
        'form': form,
        'all_lists': vacations_list_all
    })


def schedules_compare(request):
    if request.method == 'POST':
        form = CompareVacationsListForm(owner=request.user, data=request.POST)
        if form.is_valid():
            first_list_id = request.POST['first_list']
            department_name = request.user.get_group_name()
            second_list_id = request.POST['second_list']
            first_vacations_list = VacationsList.objects.get(id=first_list_id)
            if request.POST['second_list'] == '':
                data = first_vacations_list.compare_with_online_schedule(department_name)
            else:
                second_vacations_list = VacationsList.objects.get(id=second_list_id)
                data = first_vacations_list.compare_two_list(second_vacations_list)
            request.session['data'] = data
            return render(request, 'compare_schedules.html', {
                'data': data,
            })
    return redirect('schedule:schedule_list')

def delete_list(request, list_name):
    if VacationsList.objects.filter(owner=request.user, name=list_name).exists():
        vacations_list = VacationsList.objects.get(owner=request.user, name=list_name)
        vacations_list.remove()
    return redirect('schedule:schedule_list')

@login_required
def schedule_download(request, category):
    file_name = str(now())[0:10]
    user_name = str(request.user.id)
    file_path = "uploads/schedule/%s" % user_name
    with open(file_path, 'w', newline='\n') as csvfile:
        fieldnames = ['user_name', 'vacation_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writerows(request.session['data'][category])
    with open(file_path, 'r') as csvfile:
        response = HttpResponse(csvfile.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s_%s.csv"' % (category, file_name)
    return response