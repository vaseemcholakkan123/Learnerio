# Generated by Django 4.1.7 on 2023-03-14 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0009_course_chapters_course_language_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='chapters',
            field=models.IntegerField(choices=[(2, '2 chapters'), (3, '3 chapters'), (4, '4 chapters'), (5, '5 chapters'), (6, '6 chapters'), (7, '7 chapters'), (8, '8 chapters'), (9, '9 chapters'), (10, '10 chapters')], null=True),
        ),
    ]