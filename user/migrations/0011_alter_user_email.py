# Generated by Django 3.2.7 on 2021-10-17 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0010_auto_20211017_1626"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="email"),
        ),
    ]