from core.models import UUIDChronoModel
from django.db import models


class Sale(UUIDChronoModel):
    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Dinheiro'
        CREDIT = 'CREDIT', 'Cartão de Crédito'
        DEBIT = 'DEBIT', 'Cartão de Débito'
        PIX = 'PIX', 'Transferência PIX'
        BOLETO = 'BOLETO', 'Boleto'

    business = models.ForeignKey('management.Business', on_delete=models.CASCADE)
    created_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_sales')
    client = models.ForeignKey('management.Client', on_delete=models.SET_NULL, blank=True, null=True, related_name='sales')
    payment = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
