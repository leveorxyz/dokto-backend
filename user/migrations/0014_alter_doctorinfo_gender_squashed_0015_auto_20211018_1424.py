# Generated by Django 3.2.7 on 2021-10-18 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0013_alter_user_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctorinfo",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("MALE", "male"), ("FEMALE", "female"), ("OTHER", "other")],
                max_length=7,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="doctorinfo",
            name="identification_number",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="doctorinfo",
            name="identification_photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="identification_photo"
            ),
        ),
        migrations.AddField(
            model_name="doctorinfo",
            name="identification_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("PASSPORT", "passport"),
                    ("DRIVER'S LICENSE", "driver's license"),
                    ("STATE ID", "state id"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
