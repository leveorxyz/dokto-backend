# Generated by Django 3.2.7 on 2021-11-04 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0032_doctorinfo_identification_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patientinfo",
            name="gender",
            field=models.CharField(
                choices=[
                    ("MALE", "male"),
                    ("FEMALE", "female"),
                    ("OTHER", "other"),
                    ("PREFER NOT TO SAY", "preder not to say"),
                ],
                max_length=20,
            ),
        ),
    ]