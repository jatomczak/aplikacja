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
            user.token = account_activation_token.make_token(user)
            user.save()

            current_site = get_current_site(request)
            subject = 'Zostałeś zarejestrowany'
            message = render_to_string('activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
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
    messages.info(request, "Zostałeś poprawnie zalogowany")
    next_page = request.POST.get('next', '/')
    return HttpResponseRedirect(next_page)


def activate(request, id, token):
    try:
        uid = force_text(urlsafe_base64_decode(id))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.save()
        login(request, user)
        messages.info(request, "Konto zostało potwierdzone. Zostałeś zalogowany.")
    else:
        messages.info(request, "Nieprawidłowy link potwierdzający.")
    return redirect(reverse('sandwiches:sandwiches'))
