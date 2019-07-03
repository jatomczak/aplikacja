from django.test import TestCase

from schedule import forms


class ScheduleFormTest(TestCase):
    def test_incorrect_date_range(self):
        form = forms.SelectTimeRangeForm(data={'date_from':'2019-02-10', 'date_to':'2019-02-01'})
        self.assertFalse(form.is_valid())