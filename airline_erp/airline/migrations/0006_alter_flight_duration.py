# Generated by Django 4.1.1 on 2022-09-26 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0005_flight_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='duration',
            field=models.DurationField(null=True),
        ),
    ]
