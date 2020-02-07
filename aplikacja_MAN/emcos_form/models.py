from django.db import models


class Factory(models.Model):
    factory_name = models.CharField(max_length=30, unique=True, null=False)
    factory_letter = models.CharField(max_length=1, unique=True, null=False)

    def __str__(self):
        return self.factory_name

class TaskType(models.Model):
    task_type = models.CharField(max_length=50, unique=True, null=False)
    task_type_text = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.task_type


class Bus(models.Model):
    bus_nr = models.CharField(max_length=20, null=True)
    lub_nr = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    fassung_date = models.DateField(null=True)
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, null=True)

class EmcosTask(Bus):
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)