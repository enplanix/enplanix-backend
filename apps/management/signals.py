from django.db.models import signals
from django.dispatch import receiver

from apps.management.utils import generate_business_categories


@receiver(signals.post_save, sender='business.Business')
def add_business_default_categories(instance, created=True, **kwargs):
    if created:
        print('created')
        generate_business_categories()