# Generated by Django 4.1.7 on 2023-03-18 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0014_course_requirements_course_whats_learning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='requirements',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='whats_learning',
            field=models.TextField(),
        ),
    ]
