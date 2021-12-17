# Generated by Django 3.2.7 on 2021-12-07 14:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("ehr", "0004_icds"),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientProcedure",
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
                ("type", models.CharField(blank=True, max_length=125, null=True)),
                ("code", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=512, null=True),
                ),
                ("status", models.CharField(blank=True, max_length=125, null=True)),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "patient_encounter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ehr.patientencounters",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FunctionalAndCognitiveStatus",
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
                ("moduleType", models.CharField(blank=True, max_length=125, null=True)),
                ("codeType", models.CharField(blank=True, max_length=125, null=True)),
                ("status", models.CharField(blank=True, max_length=125, null=True)),
                ("code", models.CharField(blank=True, max_length=100, null=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=512, null=True),
                ),
                (
                    "patient_encounter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ehr.patientencounters",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ChiefComplaintsAndHPI",
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
                (
                    "chiefComplaint",
                    models.CharField(blank=True, max_length=125, null=True),
                ),
                ("location", models.CharField(blank=True, max_length=100, null=True)),
                ("severity", models.CharField(blank=True, max_length=125, null=True)),
                ("duration", models.CharField(blank=True, max_length=125, null=True)),
                (
                    "modifying_factors",
                    models.CharField(blank=True, max_length=125, null=True),
                ),
                (
                    "associated_symptons",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=512, null=True),
                ),
                ("context", models.CharField(blank=True, max_length=100, null=True)),
                ("hpi", models.CharField(blank=True, max_length=512, null=True)),
                (
                    "patient_encounter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ehr.patientencounters",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
