# Generated by Django 3.2.7 on 2021-10-21 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0021_pharmacyinfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctorexperience",
            name="doctor_info",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="user.doctorinfo",
            ),
        ),
    ]
