from django.apps import apps
from django.db import models

from apps.upload.models import FileUpload, ImageUpload


def _delete_unused_models(model_class):
    used_image_ids = set()

    for model in apps.get_models():
        for field in model._meta.get_fields():
            if isinstance(field, (models.ForeignKey, models.ManyToManyField)) and field.related_model == model_class:
                if isinstance(field, models.ForeignKey):
                    used_image_ids.update(
                        model.objects.values_list(field.name, flat=True).exclude(**{field.name: None})
                    )
                elif isinstance(field, models.ManyToManyField):
                    used_image_ids.update(
                        field.related_model.objects.filter(
                            id__in=model.objects.values_list(field.name, flat=True)
                        ).values_list('id', flat=True)
                    )

    unused_images = model_class.objects.exclude(id__in=used_image_ids)
    unused_images_count = unused_images.count()

    for image in unused_images:
        image.file.delete(save=False)
        image.delete()

    return unused_images_count


def delete_unused_images():
    return _delete_unused_models(ImageUpload)


def delete_unused_files():
    return _delete_unused_models(FileUpload)