from django.test import TestCase
from django.utils import timezone

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

    def test_correct_fill_form(self):
        form = forms.SelectTimeRangeForm(data={'date_from': '2019-02-10', 'date_to': '2019-02-12'})
        self.assertTrue(form.is_valid())
        self.assertEqual({}, form.errors)

    def test_defaults_values(self):
        form = forms.SelectTimeRangeForm()
        print(form)
        date_from = form['date_from'].value()
        date_to = form['date_to'].value()
        self.assertEqual(date_from.date(), timezone.now().date())
        self.assertEqual(date_to.date(), timezone.now().date())