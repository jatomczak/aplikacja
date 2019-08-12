# Generated by Django 2.1.5 on 2019-08-07 08:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0010_auto_20190807_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacationdetails',
            name='vacation_date',
            field=models.DateField(default=datetime.datetime(2019, 8, 7, 8, 4, 33, 133896, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2019, 8, 7, 8, 4, 33, 132863, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2019, 8, 7, 8, 4, 33, 133395, tzinfo=utc)),
        ),
    ]