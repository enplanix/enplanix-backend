from django.db import models
from core.models import UUIDChronoModel, UUIDModel
from apps.business.models import Business


class AccessPreference(UUIDChronoModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE, related_name='preference')
    current_business = models.ForeignKey(Business, on_delete=models.SET_NULL, blank=True, null=True, related_name='preferences')

class UserPreference(UUIDModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE, related_name='profile_preference')
    avatar = models.ForeignKey('upload.ImageUpload', related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, default='#FFFFFF')