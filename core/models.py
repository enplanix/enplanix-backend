from django.db import models
import uuid


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class ChronoModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDChronoModel(UUIDModel, ChronoModel):
    class Meta:
        abstract = True


class AddressedModel(UUIDModel):
    address = models.CharField(max_length=255, blank=True)
    cep = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True