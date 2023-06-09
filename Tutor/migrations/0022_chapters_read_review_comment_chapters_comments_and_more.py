# Generated by Django 4.1.7 on 2023-03-20 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Tutor', '0021_categories_remove_course_category_skills_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapters',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chapters',
            name='comments',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Tutor.comment'),
        ),
        migrations.AddField(
            model_name='course',
            name='reviews',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Tutor.review'),
        ),
    ]
