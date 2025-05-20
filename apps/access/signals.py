from django.db.models import signals
from django.dispatch import receiver

from apps.access.models import AccessPreference, UserPreference

@receiver(signals.post_save, sender='account.User')
def create_default_preferences(sender, instance, created=False, **kwargs):
    if created:
        AccessPreference.objects.create(user=instance)
        UserPreference.objects.create(user=instance)