# Generated by Django 3.2.7 on 2021-11-07 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0038_auto_20211106_1440"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctorinfo",
            name="accepted_insurance",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
