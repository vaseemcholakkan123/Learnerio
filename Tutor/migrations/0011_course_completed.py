# Generated by Django 4.1.7 on 2023-03-15 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0010_alter_course_chapters'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
