# Generated by Django 2.1.5 on 2019-08-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('okbv', '0004_okbvfile_is_file_processing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='okbvfile',
            name='name',
            field=models.CharField(default='test', max_length=50),
        ),
    ]
