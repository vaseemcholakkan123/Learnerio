# Generated by Django 4.1.7 on 2023-03-21 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0043_comment_posted_date_review_posted_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='posted_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='posted_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
