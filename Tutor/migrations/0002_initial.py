# Generated by Django 4.1.7 on 2023-02-25 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Tutor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutor.tutor'),
        ),
        migrations.AddField(
            model_name='course',
            name='skills_offering',
            field=models.ManyToManyField(to='Tutor.skills'),
        ),
    ]
