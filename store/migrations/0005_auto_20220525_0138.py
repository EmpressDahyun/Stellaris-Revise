# Generated by Django 3.2 on 2022-05-24 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_reservation_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='pax',
            field=models.CharField(choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50')], default=30, max_length=13, verbose_name='Number of Guest'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pax_expected',
            field=models.CharField(choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50')], default=30, max_length=13, verbose_name='Number of Walk-in Guest'),
        ),
    ]