from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError

from clients.models import User
from schedule.models import VacationsList, VacationDetails

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