# Generated by Django 4.1.1 on 2022-09-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0009_ticket_n_bags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='n_bags',
            field=models.IntegerField(),
        ),
    ]
