from django.test import TestCase

from schedule import forms


class SelectTimeRangeFormTest(TestCase):
    def test_incorrect_date_range(self):
        form = forms.SelectTimeRangeForm(data={'date_from':'2019-02-10', 'date_to':'2019-02-01'})
        self.assertFalse(form.is_valid())
        self.assertIn("Blędny zakres dat", form.errors['date_to'])

    def test_too_long_date_range(self):
        form = forms.SelectTimeRangeForm(data={'date_from':'2019-01-01', 'date_to':'2019-10-10'})
        self.assertFalse(form.is_valid())
        self.assertIn('Maksymalny przedział nie może być dłuższy niż 31 dni.', form.errors['date_to'])

    def test_incorrect_date_format(self):
        form = forms.SelectTimeRangeForm(data={'date_from': '10-10-2019', 'date_to': '10-10-2019'})
        self.assertFalse(form.is_valid())
        self.assertIn('Bledny format daty', form.errors['date_from'])
        self.assertIn('Bledny format daty', form.errors['date_to'])