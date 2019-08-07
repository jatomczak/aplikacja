# Generated by Django 2.1.5 on 2019-08-07 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import okbv.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OkbvFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='uploads/okbv', validators=[okbv.models.FileExtensionValidator_PL(allowed_extensions=['csv'])])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='okbvfile',
            unique_together={('owner', 'name')},
        ),
    ]
