# Generated by Django 4.1.7 on 2023-03-18 04:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('User', '0010_alter_cart_course_id_alter_wishlist_course_id'),
        ('Admin', '0006_alter_order_order_cart'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='Orders',
        ),
    ]
