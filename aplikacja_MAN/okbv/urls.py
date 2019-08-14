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
    path('files_list/<file_name>/from_db', views.show_data_from_db , name='data_from_db'),
    path('files_list/<file_name>/from_file', views.show_data_from_file , name='data_from_file'),
]
