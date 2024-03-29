from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm

def logout_view(request):
    logout(request)
    messages.info(request, "Zostałeś poprawnie wylogowany")
    return HttpResponseRedirect(request.GET.get('next', '/'))


def add_new_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('clients:login'))
        else:
            return render(request, 'add_new_user.html',{
                'form': form
            })
    return render(request, 'add_new_user.html', {
        'form': form
    })


@login_required()
def login_view(request):
    next_page = request.POST.get('next', '/')
    return HttpResponseRedirect(next_page)

