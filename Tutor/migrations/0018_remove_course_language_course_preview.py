# Generated by Django 4.1.7 on 2023-03-19 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0017_alter_course_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='language',
        ),
        migrations.AddField(
            model_name='course',
            name='preview',
            field=models.FileField(default='', upload_to='course_previews'),
        ),
    ]
