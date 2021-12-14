# Generated by Django 3.2.7 on 2021-12-10 09:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0004_passwordresetwhitelist"),
    ]

    operations = [
        migrations.CreateModel(
            name="WaitingRoom",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("text", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "room_media",
                    models.FileField(
                        blank=True, null=True, upload_to="doctor_waiting_room_media"
                    ),
                ),
                (
                    "doctor",
                    models.OneToOneField(
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