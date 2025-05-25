import decimal
from django.core.validators import MinValueValidator
from apps.sale.choices import SalePaymentMethod, SaleStatusChoices, SaleTypeChoices
from core.managers import CustomManager
from core.models import UUIDChronoModel
from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

class Sale(UUIDChronoModel):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    created_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_sales')
    client = models.ForeignKey('management.Client', on_delete=models.SET_NULL, blank=True, null=True, related_name='sales')
    payment = models.CharField(max_length=20, choices=SalePaymentMethod.choices, default=SalePaymentMethod.CASH)
    status = models.CharField(max_length=20, choices=SaleStatusChoices.choices, default=SaleStatusChoices.PENDING)
    total_price = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    agenda_extra = models.OneToOneField('agenda.AgendaExtra', on_delete=models.SET_NULL, blank=True, null=True)

    objects: CustomManager = CustomManager()
    
    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.agenda_extra:
            self.client = self.agenda_extra.client
        super().save(*args, **kwargs) 

    def update_total_price(self):
        self.total_price = self.sale_items.annotate(
        total=ExpressionWrapper(
            F('snapshot_price') * F('quantity'),
            output_field=DecimalField()
        )).aggregate(
            total_sum=Coalesce(Sum('total'), decimal.Decimal('0.00'))
        )['total_sum']
        Sale.objects.filter(id=self.id).update(total_price=self.total_price)


class SaleItem(UUIDChronoModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_items')
    type = models.CharField(max_length=16, choices=SaleTypeChoices.choices)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    snapshot_name = models.CharField(max_length=255)
    snapshot_code = models.CharField(max_length=33)
    snapshot_price = models.DecimalField(max_digits=15, decimal_places=3)
    origin = models.ForeignKey('management.Offer', on_delete=models.SET_NULL, null=True)

    objects: CustomManager = CustomManager(business_field='sale__business')
    
    def save(self, *args, **kwargs):
        self.snapshot_name = self.origin.name
        self.snapshot_price = self.origin.price
        self.snapshot_code = self.origin.code
        return super().save(*args, **kwargs)
