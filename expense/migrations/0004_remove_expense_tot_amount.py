# Generated by Django 2.2 on 2020-10-23 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_auto_20201023_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='tot_amount',
        ),
    ]
