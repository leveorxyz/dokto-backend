# Generated by Django 3.2.7 on 2022-01-05 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='appointment.appointment'),
        ),
    ]