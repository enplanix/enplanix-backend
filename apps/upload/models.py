from apps import upload
from core.models import UUIDChronoModel
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os 

from django.conf import settings

# TODO: CHECK FOR FUTURE PERFORMANCE IMPROVEMENTS
# https://stackoverflow.com/questions/71116738/how-to-use-celery-to-upload-files-in-django

# Whenever you update this settings, update frontend config.js as well
FILE_MAX_SIZE = 5 * 1024 * 1024
FILE_EXTENSION_VALIDATOR = FileExtensionValidator(["pdf", "txt"])
IMAGE_EXTENSION_VALIDATOR = FileExtensionValidator(["png", "jpg", "jpeg"])

def upload_to_using_model_uuid(instance, filename):
    ext = filename.split('.')[-1]
    today = timezone.now().strftime('%m/%Y')
    unique_id = str(instance.id)
    return os.path.join(today, f"{unique_id}.{ext}")


def validate_file_size(value):
    if value.size > FILE_MAX_SIZE:
        raise ValidationError("O tamanho do arquivo é maior que o permitido")


class BaseFileUpload(UUIDChronoModel):
    file = models.FileField(validators=[validate_file_size, FILE_EXTENSION_VALIDATOR], upload_to=upload_to_using_model_uuid)
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class FileUpload(BaseFileUpload):
    pass


class ImageUpload(BaseFileUpload):
    file = models.ImageField(validators=[validate_file_size, IMAGE_EXTENSION_VALIDATOR], upload_to=upload_to_using_model_uuid)