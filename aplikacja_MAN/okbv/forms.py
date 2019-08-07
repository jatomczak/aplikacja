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

    # def clean_file(self):
        # unique_list = []
        # file = self.cleaned_data.get('file')
        # for num_line, line in enumerate(file):
        #     decode_line = line.decode('utf-8')
        #     split_line = decode_line.split(';')
        #     if split_line.__len__() != 4:
        #         raise forms.ValidationError('PLIK NIE POSIADA ODPOWIEDNIJ LICZBY KOLUMN - LINIA %d' % (num_line + 1))
        #     unique_element = split_line[3]
        #     unique_list.append(unique_element)
        #     if len(unique_list) != len(set(unique_list)):
        #         raise forms.ValidationError('PLIK ZAWIERA DUPLIKATY W KOLUMNIE CZWARTEJ - LINIA %d' % (num_line + 1))
        #     try:
        #         datetime.strptime(split_line[1], self.DATE_FORMAT)
        #     except ValueError:
        #         raise forms.ValidationError('\'%s\' - BLEDNY FORMAT DATY - LINIA %d' %(split_line[1], (num_line + 1)))
        # return file