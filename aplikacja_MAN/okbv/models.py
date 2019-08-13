from django.db import models
from django.core.validators import FileExtensionValidator
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
        'lub_nr': 'LUB_NR',
        'version': 'VERSION',
        'type': 'NACHTRAG_TYPE',
        'status': 'NACHTRAG_STATUS',
    }
    file_path = UPLOAD_FILE_PATH + 'okbv'
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=file_path, validators=[FileExtensionValidator_PL(allowed_extensions=['csv'])])

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
                bus.save()
                bus.create_nachtrag(cursor)

    def compare_file_with_db(self):
        return model_to_dict(self)

class Bus(models.Model):
    bus_nr = models.CharField(max_length=20, null=True)
    lub_nr = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    t1 = models.DateField(null=True)
    from_file = models.ForeignKey(OkbvFile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('from_file', 'lub_nr')

    def set_t1(self, cursor):
        query = "select DATUM_IST from Beom.iwh_meilensteine where lub_nr ='%s' and MEILENSTEIN='T1'"
        cursor.execute(query % self.lub_nr)
        result = cursor.fetchall()
        if len(result):
            if len(result[0]):
                self.t1 = result[0][0]

    def create_nachtrag(self, cursor):
        query = "select LUB_NR, VERSION_NR, GEWERK_NAME, STATUS, STAT_USER, STATUS_DATUM " \
                "from Beom.iwh_gewerke where lub_nr ='%s' and " \
                "(GEWERK_NAME = 'IBIS' or GEWERK_NAME='Elektrik')"
        cursor.execute(query % self.lub_nr)
        result = cursor.fetchall()
        for [_, version, type, status, user, date] in result:
            nachtrag = Nachtrag()
            nachtrag.bus = self
            nachtrag.version = version
            nachtrag.type = type
            nachtrag.status = status
            nachtrag.user = user
            nachtrag.status_date = date
            nachtrag.save()


class Nachtrag(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    version = models.IntegerField()
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=30)
    user = models.CharField(max_length=10, null=True)
    status_date = models.DateField(null=True)

    class Meta:
        unique_together = ('bus', 'version', 'type')

