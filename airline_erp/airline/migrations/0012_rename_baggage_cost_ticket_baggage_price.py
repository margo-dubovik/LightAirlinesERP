# Generated by Django 4.1.1 on 2022-09-26 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0011_comfortsprice_delete_baggageprice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='baggage_cost',
            new_name='baggage_price',
        ),
    ]
