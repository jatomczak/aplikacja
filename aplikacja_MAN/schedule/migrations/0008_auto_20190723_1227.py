# Generated by Django 2.1.5 on 2019-07-23 10:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import schedule.models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20190627_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacationdetails',
            name='vacation_date',
            field=models.DateField(default=datetime.datetime(2019, 7, 23, 10, 27, 17, 921488, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationslist',
            name='file',
            field=models.FileField(upload_to='uploads/schedule', validators=[schedule.models.FileExtensionValidator_PL(allowed_extensions=['csv'])]),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2019, 7, 23, 10, 27, 17, 920459, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2019, 7, 23, 10, 27, 17, 920459, tzinfo=utc)),
        ),
    ]