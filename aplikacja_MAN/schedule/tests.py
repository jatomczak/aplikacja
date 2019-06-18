from django.test import TestCase
from clients.models import User, Group
from unittest.mock import MagicMock, PropertyMock

class TestScheduleViews(TestCase):
    def setUp(self):
        group_ibis = Group(group_name='IBIS', coordinator_name='JAN')
        group_ibis.save()
        user = User(email='test@test.pl', group=group_ibis)
        user.set_password('test')
        user.save()

    def test_objects_model_created_correctly(self):
        users_list = User.objects.all()
        groups_list = Group.objects.all()
        self.assertEqual(users_list.count(), 1)
        self.assertEqual(groups_list.count(), 1)


    def test_correct_loaded(self):
        self.client.login(email='test@test.pl', password='test')
        response = self.client.get('/harmonogram/')
        self.assertIn(b'HARMONOGRAM', response.content)

    def test_home_view_used_home_template(self):
        self.client.login(email='test@test.pl', password='test')
        response = self.client.get('/harmonogram/')
        self.assertTemplateUsed(response, 'home.html')