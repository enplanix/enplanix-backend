from django.core.validators import MinValueValidator
from core.models import UUIDChronoModel, UUIDModel
from django.db import models
from django.db.models import Sum, F

class Sale(UUIDChronoModel):
    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Dinheiro'
        CREDIT = 'CREDIT', 'Cartão de Crédito'
        DEBIT = 'DEBIT', 'Cartão de Débito'
        PIX = 'PIX', 'Transferência PIX'
        BOLETO = 'BOLETO', 'Boleto'

    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pendente',
        APPROVED = 'COMPLETED', 'Completada'
        CANCELED = 'CANCELED', 'Cancelada'

    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    created_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_sales')
    client = models.ForeignKey('management.Client', on_delete=models.SET_NULL, blank=True, null=True, related_name='sales')
    payment = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    total_price = models.DecimalField(max_digits=15, decimal_places=3, default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def update_total_price(self):
        self.total_price = self.sale_items.aggregate(total=Sum('snapshot_price') * F('quantity'))['total']


class SaleItem(UUIDModel):
    class TypeChoices(models.TextChoices):
        PRODUCT = 'PRODUCT', 'Product'
        SERVICE = 'SERVICE', 'Service'

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_items')
    type = models.CharField(max_length=16, choices=TypeChoices.choices)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    snapshot_name = models.CharField(max_length=255)
    snapshot_code = models.CharField(max_length=33)
    snapshot_price = models.DecimalField(max_digits=15, decimal_places=3)
    
    def save(self, *args, **kwargs):
        self.snapshot_name = self.origin.name
        self.snapshot_price = self.origin.price
        self.snapshot_code = self.origin.code
        return super().save(*args, **kwargs)

class ProductSaleItem(SaleItem):
    origin = models.ForeignKey('management.Product', on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.type = SaleItem.TypeChoices.PRODUCT
        return super().save(*args, **kwargs)


class ServiceSaleItem(SaleItem):
    origin = models.ForeignKey('management.Service', on_delete=models.SET_NULL, blank=True, null=True)
     
    def save(self, *args, **kwargs):
        self.type = SaleItem.TypeChoices.SERVICE
        return super().save(*args, **kwargs)