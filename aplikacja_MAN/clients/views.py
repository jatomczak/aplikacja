from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from .forms import RegisterForm
from .models import User


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
            messages.info(request, "Zostałeś zarejestrowany, kliknij w link w mailu, by potwierdzić konto")

            user = User.objects.filter(('email', request.POST['email'])).first()
            user.save()

            return redirect('login')
        else:
            return render(request, 'add_new_user.html',{
                'form': form
            })
    return render(request, 'add_new_user.html', {
        'form': form
    })


@login_required()
def login_view(request):
    # messages.info(request, "Zostałeś poprawnie zalogowany")
    # next_page = request.POST.get('next', '/')
    # return HttpResponseRedirect(next_page)
    return HttpResponse('test')

