# Generated by Django 3.2 on 2022-05-28 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_remove_order_customer_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='remarks',
            field=models.TextField(blank=True, verbose_name='Remarks'),
        ),
    ]