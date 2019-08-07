from django.urls import path

from . import views

app_name = 'okbv'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
]
