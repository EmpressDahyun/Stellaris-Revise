# Generated by Django 3.2 on 2022-05-28 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20220528_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_remarks',
            field=models.TextField(default=1, verbose_name='Customer Remarks'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CustomerNotes',
        ),
    ]
