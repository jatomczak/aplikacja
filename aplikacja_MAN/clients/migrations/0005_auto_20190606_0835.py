# Generated by Django 2.1.5 on 2019-06-06 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20190606_0818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='coorinator_name',
            new_name='coordinator_name',
        ),
    ]
