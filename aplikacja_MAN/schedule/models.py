from django.db import models
from django.utils import timezone
from clients.models import User
# Create your models here.

class VacationTimeRangeModel(models.Model):
    date_from = models.DateField(default=timezone.now())
    date_to = models.DateField(default=timezone.now())

class VacationsList(VacationTimeRangeModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('owner', 'name')

class VacationDetails(models.Model):
    vacation_date = models.DateField(default=timezone.now())
    user_name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100)
    hours = models.CharField(max_length=10)
    list = models.ForeignKey(VacationsList, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('list', 'unique_id')

