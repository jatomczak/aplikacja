from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm


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
