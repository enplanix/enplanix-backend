from apps.upload.models import ImageUpload
from core.models import AddressedModel, UUIDChronoModel, UUIDModel
from django.db import models


class Client(UUIDChronoModel, AddressedModel):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, default='#FFFFFF')


class OfferType(models.TextChoices):
    PRODUCT = "PRODUCT", "Produto"
    SERVICE = "SERVICE", "Serviço"


class CategoryBase(UUIDModel):
    type = models.CharField(max_length=10, choices=OfferType.choices)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(CategoryBase):
    business = models.ForeignKey('business.Business', blank=True, null=True, on_delete=models.CASCADE)


class CategoryTemplate(CategoryBase):
    segment = models.ForeignKey('business.Segment', on_delete=models.CASCADE)


class Offer(UUIDChronoModel):
    business = models.ForeignKey("business.Business", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=33)
    price = models.DecimalField(max_digits=15, decimal_places=3)
    description = models.TextField(blank=True, null=True)
    display_on_catalog = models.BooleanField(default=False)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    cover = models.ForeignKey(ImageUpload, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name} / {self.business}'


class Service(Offer):
    duration = models.PositiveSmallIntegerField(blank=True, default=30)

    def save(self, *args, **kwargs):
        self.type = 'service'
        super().save(*args, **kwargs)


class Product(Offer):
    images = models.ManyToManyField(ImageUpload, blank=True)

    def save(self, *args, **kwargs):
        self.type = 'product'
        super().save(*args, **kwargs)