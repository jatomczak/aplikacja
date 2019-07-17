from django import forms


class BusNameForms(forms.Form):
    name = forms.CharField(max_length=15)
