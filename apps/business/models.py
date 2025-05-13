from django.db import models
from core.models import UUIDChronoModel, UUIDModel


class SegmentCategory(UUIDModel):
    code = models.CharField(max_length=24)
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ['name']


class Segment(UUIDModel):
    code = models.CharField(max_length=24)
    category = models.ForeignKey(SegmentCategory, on_delete=models.CASCADE, related_name='segments')
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ['name']


class Business(UUIDChronoModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    color = models.CharField(max_length=7, blank=True, default='#FFFFFF')
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    
    logo = models.ForeignKey('upload.ImageUpload', related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    cover = models.ForeignKey('upload.ImageUpload', related_name='+', on_delete=models.SET_NULL, blank=True, null=True)

    segment = models.ForeignKey(Segment, on_delete=models.PROTECT)

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