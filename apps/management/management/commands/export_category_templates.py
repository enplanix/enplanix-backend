from django.core.management.base import BaseCommand
from django.core import serializers
from apps.management.models import Category, CategoryBase, CategoryTemplate
from django.core.serializers import serialize


class Command(BaseCommand):

     def handle(self, *args, **kwargs):
        template_ids = CategoryTemplate.objects.values_list('pk', flat=True)
        categories = CategoryBase.objects.filter(pk__in=template_ids)
        combined_json = serialize('json', categories)
        with open('fixtures/categorybase.json', 'w') as f:
            f.write(combined_json)