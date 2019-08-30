from django import forms
from .models import OkbvFile


class UploadFileForm(forms.ModelForm):
    DATE_FORMAT ='%d.%m.%Y'
    user = None

    def create_upload_file_form(self, user):
        self.user = user
        if self.is_valid():
            okbv_file = self.save(commit=False)
            okbv_file.owner = user
            okbv_file.save()
            okbv_file.create_bus_object()
            return okbv_file

    class Meta:
        model = OkbvFile
        fields = ('name', 'file')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = OkbvFile.objects.filter(name=name, owner=self.user)
        if qs.exists():
            raise forms.ValidationError('Plik o podanej nazwie już istnieje')
        return name

    def clean_file(self):
        unique_list = []
        file = self.cleaned_data.get('file')
        for num_line, line in enumerate(file):
            unique_list.append(line)
            if len(unique_list) != len(set(unique_list)):
                raise forms.ValidationError('DUPLIKAT - LINIA -%s - %s'%(num_line, line.decode('utf-8')))
        return file