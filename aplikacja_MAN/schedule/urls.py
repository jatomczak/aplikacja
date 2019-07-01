from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('upload', views.upload_schedule, name='upload_schedule'),
    path('list', views.schedule_list, name='schedule_list'),
    path('compare', views.schedules_compare, name='schedules_compare')
]