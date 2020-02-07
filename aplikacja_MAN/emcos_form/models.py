from django.db import models

class Bus(models.Model):
    bus_nr = models.CharField(max_length=20, null=True)
    lub_nr = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    fassung_date = models.DateField(null=True)

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

    def create_nachtrag_from_db(self, cursor):
        query = "select LUB_NR, VERSION_NR, GEWERK_NAME, STATUS, STAT_USER, STATUS_DATUM " \
                "from Beom.iwh_gewerke where lub_nr ='%s' and " \
                "(GEWERK_NAME = 'IBIS' or GEWERK_NAME='Elektrik')"
        cursor.execute(query % self.lub_nr)
        result = cursor.fetchall()
        for [_, version, type, status, user, date] in result:
            nachtrag = NachtragFromDb()
            nachtrag.bus = self
            nachtrag.version = version
            nachtrag.type = type
            nachtrag.status = status
            nachtrag.user = user
            nachtrag.status_date = date
            nachtrag.save()
