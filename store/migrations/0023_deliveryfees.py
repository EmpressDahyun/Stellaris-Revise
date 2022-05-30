# Generated by Django 3.2 on 2022-05-29 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_remove_order_delivery_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryFees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_fee', models.PositiveIntegerField(verbose_name='Fee')),
            ],
        ),
    ]
