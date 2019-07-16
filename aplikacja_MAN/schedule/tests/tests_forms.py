from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from schedule import forms
from clients.models import User
from unittest import skip

class SelectTimeRangeFormTest(TestCase):
    def test_incorrect_date_range(self):
        form = forms.SelectTimeRangeForm(data={'date_from':'2019-02-10', 'date_to':'2019-02-01'})
        self.assertFalse(form.is_valid())
        self.assertIn("Blędny zakres dat", form.errors['date_to'])

    def test_too_long_date_range(self):
        form = forms.SelectTimeRangeForm(data={'date_from':'2019-01-01', 'date_to':'2019-10-10'})
        self.assertFalse(form.is_valid())
        self.assertIn('Maksymalny przedział nie może być dłuższy niż 31 dni.', form.errors['date_to'])

    @skip
    def test_incorrect_date_format(self):
        form = forms.SelectTimeRangeForm(data={'date_from': '10-10-2019', 'date_to': '10-10-2019'})
        self.assertFalse(form.is_valid())
        self.assertIn('Bledny format daty', form.errors['date_from'])
        self.assertIn('Bledny format daty', form.errors['date_to'])

    def test_correct_fill_form(self):
        form = forms.SelectTimeRangeForm(data={'date_from': '2019-02-10', 'date_to': '2019-02-12'})
        self.assertTrue(form.is_valid())
        self.assertEqual({}, form.errors)

    def test_defaults_values(self):
        form = forms.SelectTimeRangeForm()
        date_from = form['date_from'].value()
        date_to = form['date_to'].value()
        self.assertEqual(date_from.date(), timezone.now().date())
        self.assertEqual(date_to.date(), timezone.now().date())


class UploadFileFormTest(TestCase):
    def setUp(self):
        user = User(email='test@test.pl')
        user.set_password('test')
        user.save()

    def create_upload_file_form(self, data_dict):
        file_object = SimpleUploadedFile.from_dict(data_dict)
        form = forms.UploadFileForm(data=data_dict, files={'file': file_object})
        form.create_upload_file_form(user=User.objects.get(id=1))
        return form

    def test_none_object_as_file(self):
        data_dict = {
            'name': 'first_file',
            'date_from': '2019-01-01',
            'date_to': '2019-01-01',
        }
        file_object = None
        form = forms.UploadFileForm(data=data_dict, files={'file': file_object})
        form.create_upload_file_form(user=User.objects.get(id=1))
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['file'])

    def test_correct_fill_form(self):
        data_dict = {
            'filename': 'file.csv',
            'content': b'11;12;13;14\n 21;22;23;24',
            'name': 'first_file',
            'date_from': '2019-01-01',
            'date_to': '2019-01-01',
        }
        form = self.create_upload_file_form(data_dict)
        self.assertTrue(form.is_valid())
        self.assertEqual({}, form.errors)

    def test_non_csv_file(self):
        data_dict = {
            'filename': 'file.txt',
            'content': b'11;12;13;14\n 21;22;23;24',
            'name': 'first_file',
            'date_from': '2019-01-01',
            'date_to': '2019-01-01',
        }
        form = self.create_upload_file_form(data_dict)
        self.assertFalse(form.is_valid())
        self.assertIn('txt', form.errors['file'][0])
        self.assertIn('Niedozwolony format pliku', form.errors['file'][0])
