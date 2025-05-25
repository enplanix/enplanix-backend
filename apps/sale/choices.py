from django.db import models

class SalePaymentMethod(models.TextChoices):
    CASH = 'CASH', 'Dinheiro'
    CREDIT = 'CREDIT', 'Cartão de Crédito'
    DEBIT = 'DEBIT', 'Cartão de Débito'
    PIX = 'PIX', 'Transferência PIX'
    BOLETO = 'BOLETO', 'Boleto'

class SaleStatusChoices(models.TextChoices):
    PENDING = 'PENDING', 'Pendentes',
    COMPLETED = 'COMPLETED', 'Completadas'
    CANCELED = 'CANCELED', 'Canceladas'


class SaleTypeChoices(models.TextChoices):
    PRODUCT = 'PRODUCT', 'Product'
    SERVICE = 'SERVICE', 'Service'

