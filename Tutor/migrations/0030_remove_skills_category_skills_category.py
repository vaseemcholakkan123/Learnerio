# Generated by Django 4.1.7 on 2023-03-20 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0029_alter_course_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skills',
            name='category',
        ),
        migrations.AddField(
            model_name='skills',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Tutor.categories'),
        ),
    ]
