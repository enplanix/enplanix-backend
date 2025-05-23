from django.apps import AppConfig
import importlib

class ManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.management"

    def ready(self):
        importlib.import_module('.signals', __package__)