from django import forms
from .models import VacationTimeRangeModel
from datetime import datetime, timedelta


class SelectTimeRangeForm(forms.ModelForm):
    DATE_FORMAT = '%Y-%m-%d'

    class Meta:
        model = VacationTimeRangeModel
        fields = ('date_from', 'date_to')

    def clean_date_to(self):
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        if date_to and date_from and date_from > date_to:
            raise forms.ValidationError("Blędny zakres dat")
        return date_to

    def clean_date_from(self):
        date_from = self.cleaned_data.get('date_from')
        return date_from


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()