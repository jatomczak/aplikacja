from django.db import models
from django.core.validators import FileExtensionValidator
from aplikacja_MAN.settings import UPLOAD_FILE_PATH
from clients.models import User
from csv import DictReader


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
    file_headers = {'lub_nr': 'LUB_NR'}
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


class Bus(models.Model):
    bus_nr = models.CharField(max_length=20)
    lub_nr = models.CharField(max_length=20)
    t1 = models.DateField()
    from_file = models.ForeignKey(OkbvFile, on_delete=models.CASCADE)


