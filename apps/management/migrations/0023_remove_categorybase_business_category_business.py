# Generated by Django 5.2 on 2025-05-23 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0015_alter_segment_code'),
        ('management', '0022_category_alter_product_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorybase',
            name='business',
        ),
        migrations.AddField(
            model_name='category',
            name='business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.business'),
        ),
    ]
