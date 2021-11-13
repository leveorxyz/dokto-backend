# Generated by Django 3.2.7 on 2021-11-04 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0030_remove_patientinfo_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctorinfo",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("MALE", "male"),
                    ("FEMALE", "female"),
                    ("OTHER", "other"),
                    ("PREFER NOT TO SAY", "preder not to say"),
                ],
                max_length=30,
                null=True,
            ),
        ),
    ]