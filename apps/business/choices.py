from django.db import models

class IndicatorSizeChoices(models.TextChoices):
    SMALL = 'SMALL', 'Small'
    MEDIUM = 'MEDIUM', 'Medium'


class IndicatorFormatChoices(models.TextChoices):
    INTEGER = 'INTEGER', 'Integer'
    CURRENCY = 'CURRENCY', 'Currency'

