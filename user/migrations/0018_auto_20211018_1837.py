# Generated by Django 3.2.7 on 2021-10-18 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0017_doctorexperience_doctorspecialty"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctoreducation",
            name="certificate",
            field=models.ImageField(upload_to="doctor_education_photo"),
        ),
        migrations.AlterField(
            model_name="doctoreducation",
            name="college",
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name="doctoreducation",
            name="course",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="doctoreducation",
            name="year",
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name="doctorexperience",
            name="establishment_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="doctorexperience",
            name="job_title",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="doctorexperience",
            name="start_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="doctorspecialty",
            name="specialty",
            field=models.CharField(max_length=50),
        ),
    ]
