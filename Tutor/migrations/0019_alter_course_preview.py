# Generated by Django 4.1.7 on 2023-03-19 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0018_remove_course_language_course_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='preview',
            field=models.FileField(upload_to='course_previews'),
        ),
    ]