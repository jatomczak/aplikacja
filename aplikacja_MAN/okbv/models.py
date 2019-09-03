from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
from aplikacja_MAN.settings import UPLOAD_FILE_PATH
from clients.models import User
from csv import DictReader
from .oracle_db import UseOracleDb
from django.forms.models import model_to_dict


class FileExtensionValidator_PL(FileExtensionValidator):
    message = (
        "Niedozwolony format pliku. Format : '%(extension)s' nie jest dozwolony. "
        "Dozwolny format pliku to: '%(allowed_extensions)s'."
    )


class InsensitiveDictReader(DictReader):
    @property
    def _fieldnames(self):
        return self.__fieldnames

    @_fieldnames.setter
    def _fieldnames(self, value):
        value_upper = []
        if value:
            for item in value:
                value_upper.append(item.upper())
            self.__fieldnames = value_upper
        else:
            self.__fieldnames = value


class OkbvFile(models.Model):
    file_headers = {
        'lub_nr': 'LUB',
        'version': 'VERSION',
        'type': 'ORDER_TEAM',
        'status': 'ORDER_STATUS',
    }
    file_path = UPLOAD_FILE_PATH + 'okbv'
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=file_path, validators=[FileExtensionValidator_PL(allowed_extensions=['csv'])])
    is_file_processing = models.BooleanField(default=False)
    errors_list = models. CharField(max_length=500, default='', null=True)

    class Meta:
        unique_together = ('owner', 'name')

    def get_full_name(self):
        return self.name

    def remove(self):
        self.file.delete()
        self.delete()

    def read_file(self):
        text_file = []
        with open(self.file.path) as file:
            for line in file:
                text_file.append(line)
        return text_file

    def get_unique_lub_nr(self):
        result = []
        with open(self.file.path) as f:
            f_csv = InsensitiveDictReader(f, delimiter=';')
            for row in f_csv:
                result.append(row[self.file_headers['lub_nr']])
        return sorted(set(result))

    def create_bus_object(self):
        lub_nr_list = self.get_unique_lub_nr()
        for lub_nr in lub_nr_list:
            bus = Bus()
            bus.lub_nr = lub_nr
            bus.from_file = self
            bus.save()

    def download_data_from_db(self):
        bus_list = Bus.objects.filter(from_file=self)
        with UseOracleDb() as cursor:
            for bus in bus_list:
                bus.set_t1(cursor)
                bus.set_bus_nr_quantity_and_customer(cursor)
                bus.save()
                bus.create_nachtrag_from_db(cursor)

    def create_nachtrag_from_file(self):
        with open(self.file.path) as f:
            f_csv = InsensitiveDictReader(f, delimiter=';')
            for row in f_csv:
                lub_nr = row[self.file_headers['lub_nr']]
                version = row[self.file_headers['version']]
                type = row[self.file_headers['type']]
                status = row[self.file_headers['status']]
                bus = Bus.objects.get(lub_nr=lub_nr, from_file=self)
                if not NachtragFromFile.objects.filter(bus=bus, version=version, type=type).exists():
                    nachtrag = NachtragFromFile()
                    nachtrag.bus = bus
                    nachtrag.version = version
                    nachtrag.type = type
                    nachtrag.status = status
                    nachtrag.save()
                else:
                    self.errors_list += (str(row)+';')
                    self.save()


class Bus(models.Model):
    bus_nr = models.CharField(max_length=20, null=True)
    lub_nr = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    t1 = models.DateField(null=True)
    from_file = models.ForeignKey(OkbvFile, on_delete=models.CASCADE)
    plan_period = models.CharField(max_length=10, null=True)
    customer = models.CharField(max_length=50, null=True)

    class Meta:
        unique_together = ('from_file', 'lub_nr')

    def set_t1(self, cursor):
        query = "select DATUM_IST from Beom.iwh_meilensteine where lub_nr ='%s' and MEILENSTEIN='T1'"
        cursor.execute(query % self.lub_nr)
        result = cursor.fetchall()
        if len(result):
            if len(result[0]):
                self.t1 = result[0][0]

    def set_bus_nr_quantity_and_customer(self, cursor):
        query = "select FZNR, LOSGROESSE, KUNDE, PLANPERIODE  from Beom.iwh_auftraege where lub_nr ='%s'"
        cursor.execute(query % self.lub_nr)
        result = cursor.fetchall()
        if len(result):
            if len(result[0]):
                self.bus_nr, self.quantity, self.customer, self.plan_period = result[0]

    def create_nachtrag_from_db(self, cursor):
        query = "select G.LUB_NR, G.VERSION_NR, G.GEWERK_NAME, G.STATUS, G.STAT_USER, G.STATUS_DATUM, M.DATUM_SOLL " \
                "from Beom.iwh_gewerke G " \
                "inner join " \
                "Beom.iwh_meilensteine M " \
                "on " \
                "(M.LUB_NR = G.LUB_NR and M.VERSION_NR = G.VERSION_NR) " \
                "where " \
                "G.lub_nr ='%s' " \
                "and (G.GEWERK_NAME = 'IBIS' or G.GEWERK_NAME='Elektrik')  " \
                "and (M.MEILENSTEIN = 'T1' or M.MEILENSTEIN='Nachtrag Start')"
        cursor.execute(query % self.lub_nr)
        result = cursor.fetchall()
        for [_, version, type, status, user, date, start_date] in result:
            nachtrag = NachtragFromDb()
            nachtrag.bus = self
            nachtrag.version = version
            nachtrag.type = type
            nachtrag.status = status
            nachtrag.user = user
            nachtrag.status_date = date
            nachtrag.start_date = start_date
            nachtrag.save()


class Nachtrag(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    version = models.IntegerField()
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=30)
    user = models.CharField(max_length=10, null=True)
    status_date = models.DateField(null=True)
    start_date = models.DateField(null=True)

    class Meta:
        abstract = True
        unique_together = ('bus', 'version', 'type')

    def to_dict(self):
        return {'version': self.version,
                'type': self.type,
                'status': self.status,
                }


class NachtragFromDb(Nachtrag):
    pass


class NachtragFromFile(Nachtrag):
    pass
