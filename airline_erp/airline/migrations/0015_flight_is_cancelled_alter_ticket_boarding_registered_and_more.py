# Generated by Django 4.1.1 on 2022-09-28 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0014_alter_ticket_boarding_registered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='is_cancelled',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='boarding_registered',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='checked_in',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
