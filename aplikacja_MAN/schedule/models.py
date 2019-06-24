from django.db import models
from django.utils import timezone
# Create your models here.

class VacationTimeRangeModel(models.Model):
    date_from = models.DateField(default=timezone.now())
    date_to = models.DateField(default=timezone.now())

class VacationInProject(models.Model):
    vacation_date = models.DateField()
    user_name = models.CharField(max_length=100)
    unique_id = models.CharField(unique=True, max_length=100)
    hours = models.CharField(max_length=10)