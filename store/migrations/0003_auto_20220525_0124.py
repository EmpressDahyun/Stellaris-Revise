# Generated by Django 3.2 on 2022-05-24 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20220524_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='telephone_number',
        ),
        migrations.AddField(
            model_name='reservation',
            name='pax_expected',
            field=models.PositiveIntegerField(choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50')], default=30, verbose_name='Number of Walk-in Guest'),
        ),
        migrations.AlterField(
            model_name='deliveryinformation',
            name='barangay',
            field=models.CharField(choices=[('Ayala', 'Ayala'), ('Baliwasan', 'Baliwasan'), ('Boalan', 'Boalan'), ('Cabatangan', 'Cabatangan'), ('Calarian', 'Calarian'), ('Campo Islam', 'Campo Islam'), ('Canelar', 'Canelar'), ('Cawit', 'Cawit'), ('City Proper', 'City Proper'), ('Divisoria', 'Divisoria'), ('Guiwan', 'Guiwan'), ('Lumbangan', 'Lumbangan'), ('Lunzuran', 'Lunzuran'), ('Maasin', 'Maasin'), ('Malagutay', 'Malagutay'), ('Pasonanca', 'Pasonanca'), ('Putik\t', 'Putik'), ('Recodo', 'Recodo'), ('San Jose Cawa-cawa', 'San Jose Cawa-cawa'), ('San Jose Gusu', 'San Jose Gusu'), ('San Roque', 'San Roque'), ('Santa Maria', 'Santa Maria'), ('Santo Niño', 'Santo Niño'), ('Sinunoc', 'Sinunoc'), ('Talon-talon', 'Talon-talon'), ('Tetuan', 'Tetuan'), ('Tumaga', 'Tumaga'), ('Zambowood', 'Zambowood')], default='Ayala', max_length=150, verbose_name='Barangay'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='event_time_end',
            field=models.TimeField(verbose_name='Event Time End'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pax',
            field=models.PositiveIntegerField(choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50')], default=30, verbose_name='Number of Guest'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled')], default='Pending', max_length=50),
        ),
    ]
