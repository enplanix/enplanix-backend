from django.apps import AppConfig
import importlib

class SaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sale'

    def ready(self):
        importlib.import_module('.signals', __package__)
