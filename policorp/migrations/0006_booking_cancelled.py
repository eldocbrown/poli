# Generated by Django 3.1.2 on 2020-11-22 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policorp', '0005_availability_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
    ]