# Generated by Django 2.1.5 on 2019-08-09 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('okbv', '0002_bus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='bus_nr',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='bus',
            name='t1',
            field=models.DateField(null=True),
        ),
    ]