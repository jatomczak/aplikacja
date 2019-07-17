import datetime
from datetime import date
import holidays
from . import users_list
from datetime import datetime, timedelta
import csv
from .models import VacationDetails, VacationsList

from aplikacja_MAN.settings import UPLOAD_FILE_PATH

DATE_FORMAT = '%Y-%m-%d'

PATH_TO_USER_FILE = "\\\\Mnplposksv01\\btlp-btlpze\\Kapa-Planung Elektrik\\Harmonogram 2019\\BAZA\\%s.txt"

list_with_user_id_and_initials ={'SOFTWARE': users_list.SOFTWARE,
                                 'HARDWARE': users_list.HARDWARE,
                                 'IBIS': users_list.IBIS}


day_of_week = {'MON':0, 'THU': 1, 'WEN':2, 'THUR':3, 'FRI':4, 'SAT': 5, 'SUN':6}
type_of_holiday = {'urlopy': ['5', '6', '7','8', '16', '17', '19'],
                   'L4':['11', '13', '14'],
                   'learning': ['9'],
                   'hours_plus': '3',
                   'hours_minus': '4'}

def convert_string_to_date(date:str):
    return datetime.strptime(date, DATE_FORMAT).date()

def create_date_range_list(date_from, num_days):
    date_list = []
    for i in range(0,num_days):
        date_list.append(str(date_from + timedelta(days=i)))
    return date_list

def open_harm_file_for_user(user_id):
    return open(PATH_TO_USER_FILE % user_id, 'r')


def convert_day_of_year_to_date(day_of_year):
    first_day_of_year = date(2019,1,1)
    delta_time = timedelta(days = day_of_year)
    return first_day_of_year + delta_time


def count_day_of_year_based_on_numline(num_line):
    return num_line - 10

def is_date_in_range(day, date_from, date_to):
    if date_from <= day <= date_to:
        return True
    else:
        return False


def get_user_holiday(user_file, name_of_holiday='urlopy', date_from=date(2019,1,1), date_to=date(2019,12,31)):
    list_of_holiday = {}
    for num_of_line, line in enumerate(user_file):
        try:
            tekst_line = remove_new_line_char(line)
            day_of_year = count_day_of_year_based_on_numline(num_of_line)
            if day_of_year >= 0:
                day = convert_day_of_year_to_date(day_of_year)
                if is_date_in_range(day, date_from, date_to):
                    if not datetime.weekday(day) in [day_of_week['SAT'], day_of_week['SUN']]:
                        if not is_holiday(day):
                            if tekst_line in type_of_holiday[name_of_holiday]:
                                list_of_holiday[day.isoformat()] = 8
        except:
            list_of_holiday['ERROR'] = 'BLAD W LINI %s' % num_of_line

    return list_of_holiday


def get_overtime_hours(user_file, date_from=date(2019, 1, 1), date_to=date(2019, 12, 31)):
    list_of_overtime = {}
    for num_of_line, line in enumerate(user_file):
        try:
            day_of_year = count_day_of_year_based_on_numline(num_of_line)
            if day_of_year >= 0:
                day = convert_day_of_year_to_date(day_of_year)
                if is_date_in_range(day, date_from, date_to):
                    if ('3$' in line) or ('4$' in line):
                        if datetime.datetime.weekday(day) in [day_of_week['SAT'], day_of_week['SUN']]:
                            working_hour = float(line.split('$')[1].replace(',', '.'))
                            list_of_overtime[day.isoformat()]= working_hour
                        else:
                            working_hour = float(line.split('$')[1].replace(',', '.'))-8
                            list_of_overtime[day.isoformat()] = working_hour
        except:
            list_of_overtime['ERROR'] ='BLAD W LINI %s' % num_of_line
    return list_of_overtime


def read_file_again(user_file):
    user_file.seek(0)

def is_holiday(date):
    list_of_holidays = holidays.Polish()
    if date in list_of_holidays:
        return True
    else:
        return False

def remove_new_line_char(tekst):
    return tekst.replace('\n', '')


def get_data_from_harm_for_user(department: str, date_from=date(2019, 1, 1), date_to=date(2019, 12, 31), name_of_holiday='urlopy'):
    list_of_vacations = {}
    for user_id, surname in list_with_user_id_and_initials.get(department, {}).items():
        try:
            user_file = open_harm_file_for_user(user_id)
            list_of_vacations[surname] = get_user_holiday(
                user_file,
                name_of_holiday=name_of_holiday,
                date_from=date_from,
                date_to=date_to,
            )
        except FileNotFoundError:
            list_of_vacations[surname] = {'error':"Nie znaleziono pliku"}

    return list_of_vacations


def handle_uploaded_file(f):
    with open(UPLOAD_FILE_PATH + 'test.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class CsvToDb:
    file_path = 'test_vacations.csv'
    date_format = '%d.%m.%Y'

    def import_task(self, owner):
        with open(self.file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for vacation_date,  hours, user_name, unique_id in csv_reader:
                vacation = VacationDetails()
                vacation.vacation_date = datetime.strptime(vacation_date, self.date_format)
                vacation.user_name = user_name
                vacation.hours = hours
                vacation.unique_id = unique_id
                vacation.list = vacation_list
                vacation.save()

    def check_if_task_exist(self):
        pass
