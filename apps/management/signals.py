# from django.db.models import signals
# from django.dispatch import receiver

# from .models import Category, CategoryTemplate


# @receiver(signals.post_delete, sender='business.Business')
# def add_business_default_categories(instance, **kwargs):
#     for category in CategoryTemplate.objects.all():
#         segment = instance.segment
#         Category.objects.get_or_create(**category)
#     # ImageUpload.objects.filter(id__in=[instance.cover_id, instance.logo_id]).delete()