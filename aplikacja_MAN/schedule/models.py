from django.db import models
from django.utils import timezone
from clients.models import User
from aplikacja_MAN.settings import UPLOAD_FILE_PATH
from django.core.validators import FileExtensionValidator
from datetime import datetime
from schedule import scripts
import os
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

    def remove(self):
        self.file.delete()
        self.delete()

    def get_vacation_details(self):
        return VacationDetails.objects.filter(list=self)

    def compare_two_list(self, second_vacations_list):
        data = dict()
        data['PODOBIENSTWA'] = []
        data['BRAKUJE NA 2 LISCIE'] = []
        data['BRAKUJE NA 1 LISCIE'] = []
        vacations_from_first_list = self.get_vacation_details()
        vacations_from_second_list = second_vacations_list.get_vacation_details()

        for vacation in vacations_from_first_list:
            if vacations_from_second_list.filter(unique_id=vacation.unique_id).exists():
                data['PODOBIENSTWA'].append(vacation)
            else:
                data['BRAKUJE NA 2 LISCIE'].append(vacation)

        for vacation in vacations_from_second_list:
            if vacations_from_first_list.filter(unique_id=vacation.unique_id).exists():
                data['BRAKUJE NA 1 LISCIE'].append(vacation)
        return data

    def compare_with_online_schedule(self, department_name):
        holidays_list = scripts.get_data_from_harm_for_user(
            department=department_name,
            date_from=self.date_from,
            date_to=self.date_to,
        )
        result = {'found': [], 'not_found': [], 'new':[]}

        for name, holiday_type in holidays_list.items():
            for date_from in holiday_type['vacations']:
                item = {'user_name': name, 'vacation_date': date_from}
                if VacationDetails.objects.filter(list=self, vacation_date=date_from, user_name=name).exists():
                    result['found'].append(item)
                else:
                    result['not_found'].append(item)

        vacations_from_first_list = self.get_vacation_details()
        for vacation_details in vacations_from_first_list:
            item = dict()
            item['user_name'] = vacation_details.user_name
            item['vacation_date'] = str(vacation_details.vacation_date.isoformat())
            if not item['user_name'] in holidays_list:
                result['new'].append(item)
            elif not item['vacation_date'] in holidays_list[name]['vacations']:
                result['new'].append(item)
        return result


class VacationDetails(models.Model):
    date_format = '%d.%m.%Y'
    vacation_date = models.DateField(default=timezone.now())
    user_name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100)
    hours = models.CharField(max_length=10)
    list = models.ForeignKey(VacationsList, on_delete=models.CASCADE)

    def create_vacation_detalis(vacation_date, hours,  user_name, unique_id, vacations_list):
        vacation = VacationDetails()
        vacation.vacation_date = datetime.strptime(vacation_date, VacationDetails.date_format)
        vacation.user_name = user_name
        vacation.hours = hours
        vacation.unique_id = unique_id
        vacation.list = vacations_list
        vacation.save()
        return vacation

    class Meta:
        unique_together = ('list', 'unique_id')