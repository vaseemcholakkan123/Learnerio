# Generated by Django 4.1.7 on 2023-03-13 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_alter_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bill_amount',
            field=models.FloatField(default=0),
        ),
    ]