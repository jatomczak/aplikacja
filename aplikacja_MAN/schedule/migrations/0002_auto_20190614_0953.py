# Generated by Django 2.1.5 on 2019-06-14 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_from',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='vacationtimerangemodel',
            name='date_to',
            field=models.DateField(),
        ),
    ]
