# Generated by Django 2.1.5 on 2019-08-30 12:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20190830_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacationdetails',
            name='vacation_date',
            field=models.DateField(default=datetime.datetime(2019, 8, 30, 12, 45, 22, 328862, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2019, 8, 30, 12, 45, 22, 327852, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2019, 8, 30, 12, 45, 22, 327852, tzinfo=utc)),
        ),
    ]
