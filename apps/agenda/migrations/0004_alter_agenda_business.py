# Generated by Django 5.2 on 2025-05-10 20:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0003_agenda_business'),
        ('business', '0004_business_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.business'),
        ),
    ]
