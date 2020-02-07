from django.db import models

class Facory(models.Model):
    facotry_name = models.CharField(max_length=30, unique=True, null=False)
    factory_letter = models.CharField(max_length=1, unique=True, null=False)

class Bus(models.Model):
    bus_nr = models.CharField(max_length=20, null=True)
    lub_nr = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    fassung_date = models.DateField(null=True)
    factory = models.ForeignKey(Facory, on_delete=models.SET_NULL, null=True)

    def set_t1(self, cursor):
        query = "select DATUM_IST from Beom.iwh_meilensteine where lub_nr ='%s' and MEILENSTEIN='T1'"
        cursor.execute(query % self.lub_nr)
        result = cursor.fetchall()
        if len(result):
            if len(result[0]):
                self.t1 = result[0][0]

    def set_bus_nr(self, cursor):
        query = "select FZNR from Beom.iwh_auftraege where lub_nr ='%s'"
        cursor.execute(query % self.lub_nr)
        result = cursor.fetchall()
        if len(result):
            if len(result[0]):
                self.bus_nr = result[0][0]
