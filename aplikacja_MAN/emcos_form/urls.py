from django.urls import path
from . import views

app_name = 'emocs_form'

urlpatterns = [
    path('', views.home_view, name='home'),
]