from django import forms
from .models import VacationTimeRangeModel


class SelectTimeRangeForm(forms.ModelForm):
    class Meta:
        model = VacationTimeRangeModel
        fields = ('date_from', 'date_to')