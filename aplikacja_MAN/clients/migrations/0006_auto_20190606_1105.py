# Generated by Django 2.2.2 on 2019-06-06 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_auto_20190606_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
