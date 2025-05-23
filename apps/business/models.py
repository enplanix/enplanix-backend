from django.db import models
from core.models import UUIDChronoModel, UUIDModel
from datetime import time

class Segment(UUIDModel):
    code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    emoji = models.CharField(max_length=16)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.emoji} {self.name}'


class Business(UUIDChronoModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    color = models.CharField(max_length=7, blank=True, default='#FFFFFF')
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    
    logo = models.ForeignKey('upload.ImageUpload', related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    cover = models.ForeignKey('upload.ImageUpload', related_name='+', on_delete=models.SET_NULL, blank=True, null=True)

    segment = models.ForeignKey(Segment, on_delete=models.PROTECT, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def save(self, *args, user=None, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BusinessConfig(UUIDModel):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='config')
    agenda_start_time = models.TimeField(default=time(7, 0))
    agenda_end_time = models.TimeField(default=time(18, 0))
    agenda_allow_conflicting_time = models.BooleanField(default=False)

    def __str__(self):
        return self.business.name


class BusinessMember(UUIDChronoModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name='member_profiles')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['business', 'user'], name='unique_business_user')
        ]

    def __str__(self):
        return self.business.name