# Generated by Django 3.2 on 2022-05-28 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0008_auto_20220528_2248'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_notes', models.TextField(verbose_name='Customer Remarks')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.DeleteModel(
            name='CustomerRemarks',
        ),
        migrations.AddField(
            model_name='order',
            name='customer_remarks',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.customernotes', verbose_name='Customer Notes'),
            preserve_default=False,
        ),
    ]