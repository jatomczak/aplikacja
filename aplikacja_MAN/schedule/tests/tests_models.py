from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError
from unittest.mock import MagicMock

from clients.models import User
from schedule.models import VacationsList, VacationDetails
from schedule import scripts

class VacationDetailsTest(TestCase):
    def create_user(self):
        user = User(email='test@test.pl')
        user.set_password('test')
        user.save()

    def create_vacation_list(self):
        vacation_list = VacationsList()
        vacation_list.name = 'unique_1'
        vacation_list.owner = User.objects.get(id=1)
        vacation_list.save()

    def create_vacation_details(self):
        vacation = VacationDetails()
        vacation.unique_id = 'unique_1'
        vacation.vacation_date = timezone.now()
        vacation.list = VacationsList.objects.get(id=1)
        vacation.save()

    def setUp(self):
        self.create_user()
        self.create_vacation_list()
        self.create_vacation_details()

    def test_correct_created_objects(self):
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 1)

        all_vacations_lists = VacationsList.objects.all()
        self.assertEqual(all_vacations_lists.count(), 1)

        all_vacations = VacationDetails.objects.all()
        self.assertEqual(all_vacations.count(), 1)

    def test_no_vacation_without_list(self):
        VacationsList.objects.all().delete()
        all_vacations = VacationDetails.objects.all()
        self.assertEqual(all_vacations.count(), 0)

    def test_no_vacation_without_user(self):
        User.objects.all().delete()
        all_vacations_lists = VacationsList.objects.all()
        self.assertEqual(all_vacations_lists.count(), 0)
        all_vacations = VacationDetails.objects.all()
        self.assertEqual(all_vacations.count(), 0)

    def test_cannot_save_two_the_same_element_on_list(self):
        with self.assertRaises(IntegrityError):
            self.create_vacation_details()

    def test_two_difference_id_on_one_list(self):
        vacation = VacationDetails()
        vacation.unique_id = 'unique_2'
        vacation.vacation_date = timezone.now()
        vacation.list = VacationsList.objects.get(id=1)
        vacation.save()

    def test_the_same_element_on_two_different_list(self):
        vacation_list = VacationsList()
        vacation_list.name = 'unique_2'
        vacation_list.owner = User.objects.get(id=1)
        vacation_list.save()

        vacation = VacationDetails()
        vacation.unique_id = 'unique_1'
        vacation.vacation_date = timezone.now()
        vacation.list = VacationsList.objects.get(id=2)
        vacation.save()


class VacationsListTest(TestCase):
    def setUp(self):
        self.create_user()
        self.create_vacation_list('unique_1')
        self.create_vacation_list('unique_2')
        self.assertEqual(VacationsList.objects.count(), 2)

    def create_user(self):
        user = User(email='test@test.pl')
        user.set_password('test')
        user.save()

    def create_vacation_list(self, unique_name):
        vacation_list = VacationsList()
        vacation_list.name = unique_name
        vacation_list.date_from = '2019-01-01'
        vacation_list.date_to = '2019-01-30'
        vacation_list.owner = User.objects.get(id=1)
        vacation_list.save()

    def create_vacation_detalis(self):
        vacations_data = [
            ['01.01.2019', 8, 'Tomczak', 1],
            ['02.01.2019', 8, 'Tomczak', 2],
            ['03.01.2019', 8, 'Tomczak', 3],
            ['04.01.2019', 8, 'Tomczak', 4],
            ['05.01.2019', 8, 'Korcz', 5],
        ]
        vacations_list = VacationsList.objects.get(id=1)
        for vacation_date, hours, user_name, unique_id in vacations_data:
            VacationDetails.create_vacation_detalis(vacation_date, hours, user_name, unique_id, vacations_list)


    def test_correct_compare(self):
        vacations_list = VacationsList.objects.get(id=1)
        self.create_vacation_detalis()

        schedule_online = {'Tomczak':
            {'vacations':
                {
                '2019-01-01': 8,
                '2019-01-02': 8,
                '2019-01-03': 8,
                '2019-01-05': 8,
                }
            }}
        mock = MagicMock(return_value=schedule_online)
        scripts.get_data_from_harm_for_user = mock
        response = vacations_list.compare_with_online_schedule('IBIS')
        print(response)
        self.assertTrue({'user_name': 'Tomczak', 'vacation_date': '2019-01-01'} in response['found'])
        self.assertFalse({'user_name': 'Tomczak', 'vacation_date': '2019-01-04'} in response['found'])
        self.assertTrue({'user_name': 'Tomczak', 'vacation_date': '2019-01-04'} in response['new'], response['new'])
