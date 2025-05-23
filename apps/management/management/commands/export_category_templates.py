from django.core.management.base import BaseCommand
from django.core import serializers
from apps.management.models import Category, CategoryTemplate

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        templates = CategoryTemplate.objects.all()
        category_ids = templates.values_list('categorybase_ptr_id', flat=True)
        categories = Category.objects.filter(id__in=category_ids)
        
        data = serializers.serialize('json', list(categories) + list(templates))
        with open('fixtures/category_templates.json', 'w') as file:
            file.write(data)