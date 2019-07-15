from django.urls import path
from . import views

app_name = 'ibis'

urlpatterns = [
    path('', views.home_view),
]
