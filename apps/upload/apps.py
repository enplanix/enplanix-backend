import importlib
from django.apps import AppConfig


class UploadConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.upload"

    def ready(self):
        importlib.import_module(".signals", __package__)
