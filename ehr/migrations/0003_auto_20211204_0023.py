# Generated by Django 3.2.7 on 2021-12-03 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ehr", "0002_patientsocialhistory"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="MedicalNotes",
            new_name="PlanOfCare",
        ),
        migrations.RenameField(
            model_name="assessmentdiagnosis",
            old_name="snomed_code",
            new_name="disease_code",
        ),
        migrations.RenameField(
            model_name="assessmentdiagnosis",
            old_name="snomed_description",
            new_name="disease_description",
        ),
    ]
