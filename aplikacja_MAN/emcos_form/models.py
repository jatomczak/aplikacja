from django.db import models
from .oracle_db import UseOracleDb

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


    def set_fassung_date(self, cursor):
        query = "select fassdat from avis.a01 where fznr ='%s'"
        cursor.execute(query % self.bus_nr)
        result = cursor.fetchall()
        if len(result):
            if len(result[0]):
                self.fassung_date = result[0][0]

    def download_data_from_db(self):
        with UseOracleDb() as cursor:
            self.set_fassung_date(cursor)


class EmcosTask(Bus):
    time_quantity = models.IntegerField(default=8)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    additional_comments = models.CharField(max_length=500, null=True)