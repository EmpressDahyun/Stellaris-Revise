# Generated by Django 3.2 on 2022-05-29 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_deliveryfees_delivery_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryfees',
            name='delivery_fee',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]