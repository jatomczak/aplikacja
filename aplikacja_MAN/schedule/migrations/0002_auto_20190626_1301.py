# Generated by Django 2.1.5 on 2019-06-26 11:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacationslist',
            name='name',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vacationslist',
            name='vacationtimerangemodel_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='schedule.VacationTimeRangeModel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vacationdetails',
            name='vacation_date',
            field=models.DateField(default=datetime.datetime(2019, 6, 26, 11, 1, 0, 101120, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2019, 6, 26, 11, 1, 0, 101120, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2019, 6, 26, 11, 1, 0, 101120, tzinfo=utc)),
        ),
        migrations.RemoveField(
            model_name='vacationslist',
            name='id',
        ),
        migrations.AlterUniqueTogether(
            name='vacationslist',
            unique_together={('owner', 'name')},
        ),
    ]
