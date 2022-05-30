# Generated by Django 3.2 on 2022-05-29 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_order_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_feee',
            field=models.PositiveIntegerField(default=1, verbose_name='Delivery Fee'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sales',
            name='total_orders',
            field=models.PositiveIntegerField(verbose_name='Total Orders'),
        ),
    ]
