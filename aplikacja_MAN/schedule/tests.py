from django.test import TestCase
from django.http import HttpRequest
from django.utils import timezone
from django.db.utils import IntegrityError
from unittest.mock import MagicMock

from clients.models import User, Group
from . import views, scripts, forms
from .models import VacationsList, VacationTimeRangeModel, VacationDetails

class ScheduleFormTest(TestCase):
    def test_incorrect_date_range(self):
        form = forms.SelectTimeRangeForm(data={'date_from':'2019-02-10', 'date_to':'2019-02-01'})
        self.assertFalse(form.is_valid())


class TestScheduleViews(TestCase):
    def setUp(self):
        group_ibis = Group(group_name='IBIS', coordinator_name='JAN')
        group_ibis.save()

        user = User(email='test@test.pl', group=group_ibis)
        user.set_password('test')
        user.save()

        user_no_group = User(email='no_group@test.pl')
        user_no_group.set_password('test')
        user_no_group.save()

    def test_objects_model_created_correctly(self):
        users_list = User.objects.all()
        groups_list = Group.objects.all()
        self.assertEqual(users_list.count(), 2)
        self.assertEqual(groups_list.count(), 1)

    def test_home_view_used_home_template(self):
        self.client.login(email='no_group@test.pl', password='test')
        response = self.client.get('/harmonogram/')
        self.assertTemplateUsed(response, 'home.html')

    def test_correct_request(self):
        self.client.login(email='test@test.pl', password='test')
        request = HttpRequest()
        request.method = 'POST'
        request.POST['date_from'] = '2019-01-01'
        request.POST['date_to'] = '2019-02-02'
        request.user = User.objects.get(id=1)
        mock = MagicMock(return_value = {'Tomczak': {'2019-01-01':8, '2019-02-01':8,}})
        scripts.get_data_from_harm_for_user = mock
        response = views.home_view(request)
        self.assertIn(b'Tomczak', response.content)


class VacationDetailsTest(TestCase):
    def create_user(self):
        user = User(email='test@test.pl')
        user.set_password('test')
        user.save()

    def create_vacation_list(self):
        vacation_list = VacationsList()
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
        vacation_list.owner = User.objects.get(id=1)
        vacation_list.save()

        vacation = VacationDetails()
        vacation.unique_id = 'unique_1'
        vacation.vacation_date = timezone.now()
        vacation.list = VacationsList.objects.get(id=2)
        vacation.save()
