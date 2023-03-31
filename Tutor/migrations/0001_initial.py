# Generated by Django 4.1.7 on 2023-02-25 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='CourseImages')),
                ('duration', models.IntegerField()),
                ('Level', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Mixed', 'Mixed')], max_length=100)),
                ('Price', models.FloatField()),
                ('Rating', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(choices=[('Degree', 'Degree'), ('Msc', 'Msc Computer Science'), ('Bsc', 'Bsc Computer Science'), ('Self Taught', 'Self Studied')], max_length=100)),
                ('rating', models.BigIntegerField(default=0)),
                ('skills', models.ManyToManyField(to='Tutor.skills')),
            ],
        ),
    ]
