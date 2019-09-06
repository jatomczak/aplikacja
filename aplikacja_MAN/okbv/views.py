from builtins import filter

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import OkbvFile,Bus, NachtragFromDb, NachtragFromFile
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .oracle_db import UseOracleDb

def home(request):
    return HttpResponse('test')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        form.user = request.user
        if form.is_valid():
            form.create_upload_file_form(request.user)
            return redirect('okbv:files_list')
    else:
        form = UploadFileForm(initial={'name':str(now())[:16]})
    return render(request, 'upload_file.html', {
        'form': form,
    })


@login_required
def files_list(request):
    files_list = OkbvFile.objects.filter(owner=request.user)
    for file in files_list:
        if file.errors_list:
            file.errors_list = file.errors_list.split(';')
    return render(request, 'files_list.html', {
        'files_list': files_list,
    })


def delete_file(request, file_name):
    if OkbvFile.objects.filter(owner=request.user, name=file_name).exists():
        file = OkbvFile.objects.get(owner=request.user, name=file_name)
        file.remove()
    return redirect('okbv:files_list')


def read_file(request, file_name):
    if not OkbvFile.objects.filter(owner=request.user, name=file_name).exists():
        return redirect('okbv:files_list')

    daily_change = {'found': [], 'not_found':[]}
    result = {'new_auftrag': None, 'new_nachtrag': None}
    if request.method == 'POST':
        query = "SELECT LUB_NR, DATUM_IST " \
                "FROM Beom.iwh_meilensteine " \
                "where (DATUM_IST>=TO_DATE('%(daily_date)s', 'YYYY-MM-DD') and MEILENSTEIN='T1') " \
                "ORDER BY DATUM_IST"
        query = query % request.POST
        with UseOracleDb() as cursor:
            cursor.execute(query)
            result['new_auftrag'] = cursor.fetchall()

    file_object = OkbvFile.objects.get(owner=request.user, name=file_name)
    if result['new_auftrag']:
        for item in result['new_auftrag']:
            temp_dict = {'lub_nr':item[0],'date':item[1]}
            if Bus.objects.filter(from_file=file_object, lub_nr=item[0]).exists():
                daily_change['found'].append(temp_dict)
            else:
                daily_change['not_found'].append(temp_dict)

    text_file = file_object.read_file()
    return render(request, 'read_file.html', {
        'text_file': text_file,
        'daily_change': daily_change
    })


def start_file_processing(request, file_name):
    file_object = OkbvFile.objects.get(owner=request.user, name=file_name)
    file_object.download_data_from_db()
    file_object.create_nachtrag_from_file()
    file_object.is_file_processing = True
    file_object.save()
    return redirect('okbv:files_list')


def show_data_from_db(request, file_name):
    file_object = OkbvFile.objects.get(owner=request.user, name=file_name)
    bus_list = Bus.objects.filter(from_file=file_object)
    for bus in bus_list:
        bus.nachtrag = NachtragFromDb.objects.filter(bus=bus).order_by('version')
    return render(request, 'file_processing.html', {
        'bus_list': bus_list,
    })


def show_data_from_file(request, file_name):
    file_object = OkbvFile.objects.get(owner=request.user, name=file_name)
    bus_list = Bus.objects.filter(from_file=file_object)
    for bus in bus_list:
        bus.nachtrag = NachtragFromFile.objects.filter(bus=bus).order_by('version')
    return render(request, 'file_processing.html', {
        'bus_list': bus_list,
    })

def compare_data(request, file_name):
    file_object = OkbvFile.objects.get(owner=request.user, name=file_name)
    bus_list = Bus.objects.filter(from_file=file_object)
    new_nachtrags = []
    change_status = []
    for bus in bus_list:
        bus.nachtrag = NachtragFromDb.objects.filter(bus=bus)
        for nachtrag in bus.nachtrag:
            if not NachtragFromFile.objects.filter(bus=bus,
                                                   version=nachtrag.version,
                                                   type=nachtrag.type).exists():
                new_nachtrags.append(nachtrag)
            elif not NachtragFromFile.objects.filter(bus=bus,
                                                     version=nachtrag.version,
                                                     type=nachtrag.type,
                                                     status=nachtrag.status).exists():
                change_status.append(nachtrag)
    return render(request, 'compare_data.html', {
        'new_nachtrags': new_nachtrags,
        'change_status': change_status,
    })












