from django.apps import AppConfig
import importlib

class AccessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.access'

    def ready(self):
        importlib.import_module('.signals', __package__)