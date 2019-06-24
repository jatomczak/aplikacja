# Generated by Django 2.1.5 on 2019-06-24 09:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20190624_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacationinproject',
            name='vacation_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2019, 6, 24, 9, 27, 23, 727624, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2019, 6, 24, 9, 27, 23, 727624, tzinfo=utc)),
        ),
    ]
