# Generated by Django 5.2 on 2025-07-08 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_indicator'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='size',
            field=models.CharField(choices=[('SMALL', 'Small'), ('MEDIUM', 'Medium')], default='SMALL', max_length=255),
        ),
    ]
