from django.db import models
from django.utils import timezone
from clients.models import User
from aplikacja_MAN.settings import UPLOAD_FILE_PATH
from django.core.validators import FileExtensionValidator
# Create your models here.

class FileExtensionValidator_PL(FileExtensionValidator):
    message = (
        "Niedozwolony format pliku. Format : '%(extension)s' nie jest dozwolony. "
        "Dozwolny format pliku to: '%(allowed_extensions)s'."
    )


class VacationTimeRangeModel(models.Model):
    date_from = models.DateField(default=timezone.now())
    date_to = models.DateField(default=timezone.now())


class VacationsList(VacationTimeRangeModel):
    file_path = UPLOAD_FILE_PATH + 'schedule'
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=file_path, validators=[FileExtensionValidator_PL(allowed_extensions=['csv'])])
    class Meta:
        unique_together = ('owner', 'name')

    def get_full_name(self):
        return self.name


class VacationDetails(models.Model):
    vacation_date = models.DateField(default=timezone.now())
    user_name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100)
    hours = models.CharField(max_length=10)
    list = models.ForeignKey(VacationsList, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('list', 'unique_id')

