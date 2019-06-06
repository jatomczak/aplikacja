from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required()
def redirect_to_old_version(request):
    return redirect('http://10.131.80.125:5000/')

# Create your views here.
