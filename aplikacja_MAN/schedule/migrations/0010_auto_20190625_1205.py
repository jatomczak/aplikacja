# Generated by Django 2.1.5 on 2019-06-25 10:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_auto_20190625_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacationdetails',
            name='vacation_date',
            field=models.DateField(default=datetime.datetime(2019, 6, 25, 10, 5, 13, 668972, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2019, 6, 25, 10, 5, 13, 667968, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2019, 6, 25, 10, 5, 13, 667968, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='vacationdetails',
            unique_together={('list', 'unique_id')},
        ),
    ]
