from django.urls import path

from . import views

app_name = 'okbv'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files_list/', views.files_list, name='files_list'),
    path('files_list/<file_name>', views.read_file, name='read_file'),
    path('files_list/<file_name>/delete', views.delete_file, name='delete_file'),
    path('files_list/<file_name>/start', views.start_file_processing , name='file_proccesing'),
]
