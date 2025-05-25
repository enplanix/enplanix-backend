from django.apps import apps
from django.core.management.base import BaseCommand
import json

class Command(BaseCommand):

     def handle(self, *args, **kwargs):
        choices = {}
        blacklist = ["logentry"]
        for model in apps.get_models():
            model_name = model.__name__.lower()
            if model_name in blacklist:
                continue
            for field in model._meta.get_fields():
                if hasattr(field, "choices") and field.choices:
                    field_name = f'{model_name}_{field.name}'
                    data = [field for field in field.choices]
                    choices[field_name] = data

        with open('choices.json', 'w', encoding='utf-8') as file:
            jsondata = json.dumps(choices,  ensure_ascii=False)
            file.write(jsondata)
            