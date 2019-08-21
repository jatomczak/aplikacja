# Generated by Django 2.1.5 on 2019-08-07 08:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_auto_20190723_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacationdetails',
            name='vacation_date',
            field=models.DateField(default=datetime.datetime(2019, 8, 7, 8, 4, 17, 441692, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2019, 8, 7, 8, 4, 17, 440193, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2019, 8, 7, 8, 4, 17, 440193, tzinfo=utc)),
        ),
    ]
