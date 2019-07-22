from django.test import TestCase
from django.http import HttpRequest

from unittest import skip
from unittest.mock import MagicMock
from schedule import scripts, views
from clients.models import Group, User
from ..models import VacationsList, VacationDetails
from ..views import schedules_compare


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
        request.POST['date_to'] = '2019-01-30'
        request.user = User.objects.get(id=1)
        mock = MagicMock(return_value = {'Tomczak': {'vacations':{'2019-01-01':8, '2019-01-28':8,}}})
        scripts.get_data_from_harm_for_user = mock
        response = views.home_view(request)
        self.assertIn(b'Tomczak', response.content)


class TestSchedulesCompare(TestCase):
    def setUp(self):
        self.create_user()
        self.create_vacation_list('unique_1')
        self.create_vacation_list('unique_2')
        self.assertEqual(VacationsList.objects.count(), 2)


    def create_user(self):
        group_ibis = Group(group_name='IBIS', coordinator_name='JAN')
        group_ibis.save()
        user = User(email='test@test.pl', group=group_ibis)
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

    def test_date_range_of_first_list(self):
        request = HttpRequest()
        request.user = User.objects.get(id=1)
        request.method = 'POST'
        request.POST['first_list'] = 1
        request.POST['second_list'] = ''
        response = schedules_compare(request)
        self.assertEqual(response.status_code, 200)
