# Generated by Django 4.1.7 on 2023-03-09 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_delete_tutorrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mobile',
        ),
    ]
