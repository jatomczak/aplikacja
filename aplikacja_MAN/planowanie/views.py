from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

HOST_REDIRECT = 'http:////10.131.80.125'
PORT_REDIRECT = '5001'

@login_required()
def redirect_to_old_version(request):
    user_name = request.user.name
    # return redirect('http://10.131.80.125:5000/set_user/' + user_name)
    return redirect('%s:%s/set_user/%s'% (HOST_REDIRECT, PORT_REDIRECT, user_name))

# Create your views here.
