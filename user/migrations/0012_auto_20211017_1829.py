# Generated by Django 3.2.7 on 2021-10-17 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0011_alter_user_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doctorinfo",
            name="profile_photo",
        ),
        migrations.AddField(
            model_name="user",
            name="profile_photo",
            field=models.ImageField(blank=True, null=True, upload_to="profile_photo"),
        ),
    ]