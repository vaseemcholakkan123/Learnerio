# Generated by Django 4.1.7 on 2023-03-21 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0044_alter_comment_posted_date_alter_review_posted_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='students_enrolled',
            field=models.IntegerField(default=0),
        ),
    ]
