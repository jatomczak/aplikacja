from django import forms
from .models import EmcosTask
from .oracle_db import UseOracleDb


class BusForm(forms.ModelForm):
    class Meta:
        model = EmcosTask
        fields = '__all__'
        widgets = {
            'fassung_date': forms.DateInput(attrs={
                'type':'date',
            }),
            'additional_comments': forms.Textarea(attrs={
                'rows': 10,
                'cols': 50,
                'placeholder': 'additional comments',
            }
            )
        }
