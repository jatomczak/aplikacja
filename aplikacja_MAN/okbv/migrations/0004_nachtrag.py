# Generated by Django 2.1.5 on 2019-08-12 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('okbv', '0003_auto_20190809_0748'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nachtrag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField()),
                ('type', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=30)),
                ('user', models.CharField(max_length=10, null=True)),
                ('status_date', models.DateField(null=True)),
                ('Bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='okbv.Bus')),
            ],
        ),
    ]
