# Generated by Django 3.2.7 on 2021-12-26 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_auto_20211226_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionhistory',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
