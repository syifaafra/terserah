# Generated by Django 4.1 on 2022-10-28 23:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bin_bank', '0005_remove_myuser_email_alter_feedback_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 28, 23, 35, 59, 147907, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 28, 23, 35, 59, 146814, tzinfo=datetime.timezone.utc)),
        ),
    ]