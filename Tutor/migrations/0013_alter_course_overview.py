# Generated by Django 4.1.7 on 2023-03-18 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0012_course_overview_alter_course_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='overview',
            field=models.TextField(),
        ),
    ]
