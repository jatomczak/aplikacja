from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Factory, TaskType

class AddFacotry(admin.ModelAdmin):
    list_display = ('factory_name', 'factory_letter')

# class AddTaskType(admin.ModelAdmin):
#     list_display = '__all__'

admin.site.register(Factory, AddFacotry)
admin.site.register(TaskType)
# Register your models here.
