# Generated by Django 2.1.5 on 2020-02-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('okbv', '0008_auto_20200207_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='okbvfile',
            name='name',
            field=models.CharField(default='2020-02-07 08:42', max_length=50),
        ),
    ]
