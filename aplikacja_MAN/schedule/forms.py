from django import forms
from .models import VacationTimeRangeModel, VacationsList
from datetime import datetime, timedelta
import csv


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


class UploadFileForm(forms.ModelForm):
    user = None

    def create_upload_file_form(self, user):
        self.user = user
        if self.is_valid():
            vacations_list = self.save(commit=False)
            vacations_list.owner = user
            vacations_list.save()
            # vacations_list.check_file_has_correct_content()
            return vacations_list

    class Meta:
        model = VacationsList
        fields = ('name', 'date_from', 'date_to', 'file')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = VacationsList.objects.filter(name=name, owner=self.user)
        if qs.exists():
            raise forms.ValidationError('Lista o podanej nazwie już istnieje')
        return name

    def clean_file(self):
        unique_list = []
        file = self.cleaned_data.get('file')
        for num_line, line in enumerate(file):
            decode_line = line.decode('utf-8')
            split_line = decode_line.split(';')
            if split_line.__len__() != 4:
                raise forms.ValidationError('PLIK NIE POSIADA ODPOWIEDNIJ LICZBY KOLUMN - LINIA %d' % (num_line + 1))
            unique_element = split_line[3]
            unique_list.append(unique_element)

            if len(unique_list) != len(set(unique_list)):
                raise forms.ValidationError('PLIK ZAWIERA DUPLIKATY W KOLUMNIE CZWARTEJ - LINIA %d' % (num_line + 1))
        return file





class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class CompareVacationsListForm(forms.Form):
    first_list = UserModelChoiceField(queryset=None)
    second_list = UserModelChoiceField(queryset=None)

    def __init__(self, owner, *args, **kwargs):
        super(CompareVacationsListForm, self).__init__(*args, **kwargs)
        self.fields['first_list'].queryset = VacationsList.objects.filter(owner=owner)
        self.fields['second_list'].queryset = VacationsList.objects.filter(owner=owner)

    def clean_second_list(self):
        first_list = self.cleaned_data.get('first_list')
        second_list = self.cleaned_data.get('second_list')
        if first_list == second_list:
            raise forms.ValidationError('Nie można porownac tych samych list')
        return second_list
