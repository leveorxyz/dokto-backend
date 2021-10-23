# Generated by Django 3.2.7 on 2021-10-23 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0022_doctorexperience_doctor_info"),
    ]

    operations = [
        migrations.CreateModel(
            name="DoctorLanguage",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("language", models.CharField(max_length=20)),
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
        migrations.DeleteModel(
            name="UserLanguage",
        ),
    ]
