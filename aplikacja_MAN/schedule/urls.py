from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('upload', views.upload_schedule, name='upload_schedule'),
    path('list', views.schedule_list, name='schedule_list'),
    path('list/<list_name>/delete', views.delete_list, name='delete_list'),
    path('compare', views.schedules_compare, name='compare_schedules'),
    path('compare/download/<category>', views.schedule_download, name='download_schedule'),
]