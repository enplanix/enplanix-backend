from django.db import models
from core.models import UUIDChronoModel
from apps.business.models import Business


class AccessPreference(UUIDChronoModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE, related_name='preference')
    current_business = models.ForeignKey(Business, on_delete=models.SET_NULL, blank=True, null=True, related_name='preferences')