# Generated by Django 3.2 on 2022-05-28 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_order_user_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerremarks',
            name='remarks',
        ),
        migrations.AddField(
            model_name='customerremarks',
            name='customer_remarks',
            field=models.TextField(default=1, verbose_name='Customer Remarks'),
            preserve_default=False,
        ),
    ]