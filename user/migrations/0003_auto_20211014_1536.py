# Generated by Django 3.2.7 on 2021-10-14 15:36

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_auto_20211014_1528"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="contact_no",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="contact no"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                blank=True,
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters and digits only.",
                max_length=150,
                null=True,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="username",
            ),
        ),
    ]