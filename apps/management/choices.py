from django.db import models


class OfferType(models.TextChoices):
    PRODUCT = "PRODUCT", "Produto"
    SERVICE = "SERVICE", "Serviço"
