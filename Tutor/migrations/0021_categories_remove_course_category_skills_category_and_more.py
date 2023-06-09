# Generated by Django 4.1.7 on 2023-03-20 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0020_course_updated_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
        migrations.AddField(
            model_name='skills',
            name='category',
            field=models.ManyToManyField(to='Tutor.categories'),
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ManyToManyField(to='Tutor.categories'),
        ),
    ]
