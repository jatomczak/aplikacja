# Generated by Django 2.2.2 on 2019-08-27 08:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import schedule.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VacationTimeRangeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(default=datetime.datetime(2019, 8, 27, 8, 16, 6, 319236, tzinfo=utc))),
                ('date_to', models.DateField(default=datetime.datetime(2019, 8, 27, 8, 16, 6, 319236, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='VacationsList',
            fields=[
                ('vacationtimerangemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='schedule.VacationTimeRangeModel')),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='uploads/schedule', validators=[schedule.models.FileExtensionValidator_PL(allowed_extensions=['csv'])])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('owner', 'name')},
            },
            bases=('schedule.vacationtimerangemodel',),
        ),
        migrations.CreateModel(
            name='VacationDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacation_date', models.DateField(default=datetime.datetime(2019, 8, 27, 8, 16, 6, 319236, tzinfo=utc))),
                ('user_name', models.CharField(max_length=100)),
                ('unique_id', models.CharField(max_length=100)),
                ('hours', models.CharField(max_length=10)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.VacationsList')),
            ],
            options={
                'unique_together': {('list', 'unique_id')},
            },
        ),
    ]
