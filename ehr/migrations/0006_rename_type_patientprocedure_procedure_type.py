# Generated by Django 3.2.7 on 2021-12-07 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "ehr",
            "0005_chiefcomplaintsandhpi_functionalandcognitivestatus_patientprocedure",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="patientprocedure",
            old_name="type",
            new_name="procedure_type",
        ),
    ]
