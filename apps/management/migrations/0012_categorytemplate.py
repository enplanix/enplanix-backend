# Generated by Django 5.2 on 2025-05-23 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0015_alter_segment_code'),
        ('management', '0011_rename_duratiion_service_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTemplate',
            fields=[
                ('category_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='management.category')),
                ('segment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.segment')),
            ],
            options={
                'abstract': False,
            },
            bases=('management.category',),
        ),
    ]
