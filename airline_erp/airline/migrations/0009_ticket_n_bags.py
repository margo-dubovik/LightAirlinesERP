# Generated by Django 4.1.1 on 2022-09-26 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0008_alter_ticket_boarding_registered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='n_bags',
            field=models.IntegerField(null=True),
        ),
    ]