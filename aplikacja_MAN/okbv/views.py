from builtins import filter

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import OkbvFile,Bus


def home(request):
    return HttpResponse('test')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.create_upload_file_form(request.user)
            return redirect('okbv:home')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {
        'form': form,
    })


def files_list(request):
    files_list = OkbvFile.objects.filter(owner=request.user)
    return render(request, 'files_list.html', {
        'files_list': files_list
    })


def delete_file(request, file_name):
    if OkbvFile.objects.filter(owner=request.user, name=file_name).exists():
        file = OkbvFile.objects.get(owner=request.user, name=file_name)
        file.remove()
    return redirect('okbv:files_list')


def read_file(request, file_name):
    if not OkbvFile.objects.filter(owner=request.user, name=file_name).exists():
        return redirect('okbv:files_list')

    file_object = OkbvFile.objects.get(owner=request.user, name=file_name)
    text_file = file_object.read_file()
    return render(request, 'read_file.html', {
        'text_file': text_file
    })


def start_file_processing(request, file_name):
    file_object = OkbvFile.objects.get(owner=request.user, name=file_name)
    file_object.create_bus_object()
    bus_list = Bus.objects.filter(from_file=file_object)
    return render(request, 'file_processing.html', {
        'bus_list': bus_list
    })

