# Generated by Django 5.2 on 2025-05-10 22:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0004_alter_agenda_business'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendaextra',
            name='agenda',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extra', to='agenda.agenda'),
        ),
    ]
