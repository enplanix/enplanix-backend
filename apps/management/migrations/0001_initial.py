# Generated by Django 5.2 on 2025-05-24 22:30

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryBase',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('PRODUCT', 'Produto'), ('SERVICE', 'Serviço')], max_length=10)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=33)),
                ('price', models.DecimalField(decimal_places=3, max_digits=15)),
                ('description', models.TextField(blank=True, null=True)),
                ('display_on_catalog', models.BooleanField(default=False)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.business')),
                ('cover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='upload.imageupload')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categorybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='management.categorybase')),
                ('business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.business')),
            ],
            options={
                'abstract': False,
            },
            bases=('management.categorybase',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('cep', models.CharField(blank=True, max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('color', models.CharField(blank=True, default='#FFFFFF', max_length=7)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.business')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('offer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='management.offer')),
                ('duration', models.PositiveSmallIntegerField(blank=True, default=30)),
            ],
            options={
                'abstract': False,
            },
            bases=('management.offer',),
        ),
        migrations.AddField(
            model_name='offer',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='management.category'),
        ),
        migrations.CreateModel(
            name='CategoryTemplate',
            fields=[
                ('categorybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='management.categorybase')),
                ('segment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.segment')),
            ],
            options={
                'abstract': False,
            },
            bases=('management.categorybase',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('offer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='management.offer')),
                ('images', models.ManyToManyField(blank=True, to='upload.imageupload')),
            ],
            options={
                'abstract': False,
            },
            bases=('management.offer',),
        ),
    ]
