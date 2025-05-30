# Generated by Django 5.2 on 2025-05-24 22:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('access', '0001_initial'),
        ('business', '0001_initial'),
        ('upload', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='accesspreference',
            name='current_business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preferences', to='business.business'),
        ),
        migrations.AddField(
            model_name='accesspreference',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preference', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='avatar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='upload.imageupload'),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_preference', to=settings.AUTH_USER_MODEL),
        ),
    ]
