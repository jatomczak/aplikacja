from django import forms
from .models import EmcosTask
from .oracle_db import UseOracleDb


class BusForm(forms.ModelForm):
    class Meta:
        model = EmcosTask
        fields = '__all__'
        widgets = {}
    #
    # def set_fassung_date(self, cursor):
    #     query = "select fassdat from avis.a01 where fznr ='%s'"
    #     cursor.execute(query % self.bus_nr)
    #     result = cursor.fetchall()
    #     if len(result):
    #         if len(result[0]):
    #             self.fassung_date = result[0][0]
    #
    # def download_data_from_db(self):
    #     with UseOracleDb() as cursor:
    #         self.set_fassung_date(cursor)
