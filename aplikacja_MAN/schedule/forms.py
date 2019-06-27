from django import forms
from .models import VacationTimeRangeModel, VacationsList
from datetime import datetime, timedelta


class SelectTimeRangeForm(forms.ModelForm):
    DATE_FORMAT = '%Y-%m-%d'

    class Meta:
        model = VacationTimeRangeModel
        fields = ('date_from', 'date_to')
        labels = {
            'date_from': 'Data od',
            'date_to': 'Data do',
        }
        widgets = {
            'date_from': forms.DateInput(attrs={
                'type': 'date',
            }),
            'date_to': forms.DateInput(attrs={
                'type': 'date'
            }),
        }

    def clean_date_to(self):
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        if date_to and date_from and date_from > date_to:
            raise forms.ValidationError("Blędny zakres dat")

        if (date_to - date_from).days > 31:
            raise forms.ValidationError("Maksymalny przedział nie może być dłuższy niż 31 dni.")

        return date_to

    def clean_date_from(self):
        date_from = self.cleaned_data.get('date_from')
        return date_from


class UploadFileForm(forms.Form):
    file = forms.FileField()

    class Meta:
        model = VacationsList
        fields = ('name', 'date_from', 'date_to')