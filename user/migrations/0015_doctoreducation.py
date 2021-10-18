# Generated by Django 3.2.7 on 2021-10-18 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0014_alter_doctorinfo_gender_squashed_0015_auto_20211018_1424"),
    ]

    operations = [
        migrations.CreateModel(
            name="DoctorEducation",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("course", models.CharField(blank=True, max_length=50, null=True)),
                ("year", models.CharField(blank=True, max_length=15, null=True)),
                ("college", models.CharField(blank=True, max_length=60, null=True)),
                (
                    "certificate",
                    models.ImageField(
                        blank=True, null=True, upload_to="doctor_education_photo"
                    ),
                ),
                (
                    "doctor_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.doctorinfo",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]