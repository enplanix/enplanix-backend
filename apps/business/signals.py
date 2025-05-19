
from PIL import Image
from django.db.models import signals
from django.dispatch import receiver

from apps.business.models import BusinessMember, BusinessConfig
from apps.upload.models import ImageUpload
from core.context import current_request


@receiver(signals.post_save, sender='business.Business')
def set_additional_business_models(instance, created=False, **kwargs): 
    request = current_request.get()
    if created:
        BusinessMember.objects.create(business=instance, user=request.user)
        BusinessConfig.objects.get_or_create(business=instance)

@receiver(signals.post_delete, sender='business.Business')
def remove_business_images(instance, **kwargs):
    ImageUpload.objects.filter(id__in=[instance.cover_id, instance.logo_id]).delete()