import importlib
from django.apps import AppConfig


class BusinessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business'

    def ready(self):
        importlib.import_module('.signals', __package__)