# Generated by Django 4.1.7 on 2023-03-21 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0039_rename_text_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_reply', to='Tutor.comment'),
        ),
    ]
