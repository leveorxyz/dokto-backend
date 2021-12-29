# Generated by Django 3.2.7 on 2021-12-29 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0014_pharmacyavailablehours"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doctorinfo",
            name="country",
        ),
        migrations.AddField(
            model_name="user",
            name="country",
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]