from django.urls import path
from . import views

app_names = 'planowanie'


urlpatterns = [
    path('', views.redirect_to_old_version, name='old_version'),
]
