# Generated by Django 3.2 on 2022-05-28 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20220528_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_remarks',
            field=models.ForeignKey(blank='True', on_delete=django.db.models.deletion.CASCADE, to='store.customernotes', verbose_name='Customer Notes'),
        ),
    ]
