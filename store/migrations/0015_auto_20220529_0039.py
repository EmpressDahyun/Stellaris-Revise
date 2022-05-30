# Generated by Django 3.2 on 2022-05-28 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20220529_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='delivery_fees',
            field=models.PositiveIntegerField(default=1, verbose_name='Total Delivery Fees'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sales',
            name='subtotal',
            field=models.PositiveIntegerField(default=1, verbose_name='Total Wholesale Price'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sales',
            name='total_income',
            field=models.PositiveIntegerField(default=1, verbose_name='Total Income'),
            preserve_default=False,
        ),
    ]