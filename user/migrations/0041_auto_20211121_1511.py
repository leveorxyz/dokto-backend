# Generated by Django 3.2.7 on 2021-11-21 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_auto_20211108_1054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctoreducation',
            old_name='certificate',
            new_name='_certificate',
        ),
        migrations.RenameField(
            model_name='doctorinfo',
            old_name='identification_photo',
            new_name='_identification_photo',
        ),
        migrations.RenameField(
            model_name='doctorinfo',
            old_name='license_file',
            new_name='_license_file',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='profile_photo',
            new_name='_profile_photo',
        ),
        migrations.AlterField(
            model_name='clinicinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clinic_info', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='doctorinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_info', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pharmacyinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacy_info', to=settings.AUTH_USER_MODEL),
        ),
    ]
