# Generated by Django 3.2.7 on 2021-10-25 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0025_alter_patientinfo_insurance_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="DoctorReview",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "patient_name",
                    models.CharField(blank=True, max_length=80, null=True),
                ),
                ("star_count", models.FloatField(blank=True, null=True)),
                ("comment", models.TextField(blank=True, max_length=5000, null=True)),
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
        migrations.CreateModel(
            name="DoctorAvailableHours",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "day_of_week",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("SUN", "sunday"),
                            ("MON", "monday"),
                            ("TUE", "tuesday"),
                            ("WED", "wednesday"),
                            ("THU", "thursday"),
                            ("FRI", "friday"),
                            ("SAT", "saturday"),
                        ],
                        max_length=3,
                        null=True,
                    ),
                ),
                ("start_time", models.TimeField(blank=True, null=True)),
                ("end_time", models.TimeField(blank=True, null=True)),
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