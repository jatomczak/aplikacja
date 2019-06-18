from django.test import TestCase
from django.http import HttpRequest
from unittest.mock import MagicMock

from clients.models import User, Group
from . import views, scripts

class ScheduleFormTest(TestCase):
    pass

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
