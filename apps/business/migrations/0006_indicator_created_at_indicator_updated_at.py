# Generated by Django 5.2 on 2025-07-09 12:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_remove_indicator_size_indicator_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='indicator',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
