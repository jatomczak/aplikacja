"""aplikacja_MAN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from clients.forms import CustomAuthenticationForm
from .views import index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('planowanie/', include('planowanie.urls')),
    path('harmonogram/', include('schedule.urls', namespace='schedule')),
]
