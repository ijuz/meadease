# Generated by Django 5.1.1 on 2025-02-22 12:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_alter_patientdetails_doctor'),
        ('prescription', '0004_alter_prescriptions_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescriptions',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.patientdetails'),
        ),
    ]
