from django.db import models
from datetime import date

# Create your models here.
class VacationTimeRangeModel(models.Model):
    date_from = models.DateField(default=date.today())
    date_to = models.DateField(default=date.today())
