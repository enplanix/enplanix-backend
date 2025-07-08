from decimal import DivisionByZero
import babel
from django.db import models
from sympy import sympify
from apps.business.choices import IndicatorFormatChoices, IndicatorSizeChoices
from core.managers import CustomManager
from core.models import UUIDChronoModel, UUIDModel
from datetime import time
from django.utils.text import slugify
from django.utils import timezone
from dataclasses import dataclass
from django.utils import formats
from babel.numbers import format_decimal


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
    slug = models.CharField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    color = models.CharField(max_length=7, blank=True, default='#FFFFFF')
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    
    logo = models.ForeignKey('upload.ImageUpload', related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    cover = models.ForeignKey('upload.ImageUpload', related_name='+', on_delete=models.SET_NULL, blank=True, null=True)

    segment = models.ForeignKey(Segment, on_delete=models.PROTECT, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    objects: CustomManager = CustomManager(user_field='members__user')
    
    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def save(self, *args, user=None, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        return super().save(*args, **kwargs)

    def generate_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        count = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{count}'
            count += 1
        return slug
    
    def __str__(self):
        return self.name


class BusinessConfig(UUIDModel):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='config')
    agenda_start_time = models.TimeField(default=time(7, 0))
    agenda_end_time = models.TimeField(default=time(18, 0))
    agenda_allow_conflicting_time = models.BooleanField(default=False)
    objects: CustomManager = CustomManager()
    
    def __str__(self):
        return self.business.name


class BusinessMember(UUIDChronoModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name='member_profiles')
    objects: CustomManager = CustomManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['business', 'user'], name='unique_business_user')
        ]

    def __str__(self):
        return self.business.name


class Indicator(UUIDModel):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    formula = models.CharField(max_length=255)
    description = models.TextField()
    # size = models.CharField(max_length=255, choices=IndicatorSizeChoices.choices, default=IndicatorSizeChoices.SMALL)
    format = models.CharField(max_length=255, choices=IndicatorFormatChoices.choices, default=IndicatorFormatChoices.INTEGER)
    value = models.CharField(max_length=255, blank=True, null=True)

    objects: CustomManager = CustomManager()


    def calculate_value(self, variables):
        try:
            expr = sympify(self.formula)
            result = str(expr.subs(variables))
            match self.format:
                case IndicatorFormatChoices.INTEGER:
                    self.value = str(int(float(result)))
                case IndicatorFormatChoices.CURRENCY:
                    self.value = format_decimal(result, format='#,##0.00',)
                case _:
                    self.value = result
            self.save()
        except ZeroDivisionError:
            self.value = '0'
            self.save()
        except Exception as e:
            print("Error:", e)
            self.value = 'error'
            self.save()


class IndicatorCalculator:

    def __init__(self, request):
        from apps.agenda.models import Agenda
        from apps.management.models import Client, Product, Service
        from apps.sale.choices import SaleStatusChoices
        from apps.sale.models import Sale

        now = timezone.now()
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        self.request = request

        self.variables = {
            # Registry related counts
            'PRODUCTS_COUNT': Product.objects.within_request_business(request).count(),
            'SERVICES_COUNT': Service.objects.within_request_business(request).count(),

            'AGENDAS_TODAY_COUNT': Agenda.objects.within_request_business(request).filter(
                date__gte=start_of_today,
                date__lte=now,
            ).count(),

            'CLIENTS_COUNT': Client.objects.within_request_business(request).count(),

            'CLIENTS_TODAY_COUNT': Client.objects.within_request_business(request).filter(
                created_at__gte=start_of_today,
                created_at__lte=now,
            ).count(),

            # Sales related counts
            'SALES_PENDING': Sale.objects.within_request_business(request).filter(
                status=SaleStatusChoices.PENDING
            ).count(),

            'SALES_COMPLETED_COUNT': Sale.objects.within_request_business(request).filter(
                status=SaleStatusChoices.COMPLETED
            ).count(),

            'SALES_COMPLETED_TODAY_COUNT': Sale.objects.within_request_business(request).filter(
                status=SaleStatusChoices.COMPLETED,
                created_at__gte=start_of_today,
                created_at__lte=now,
            ).count(),

            'SALES_COMPLETED_MONTH_COUNT': Sale.objects.within_request_business(request).filter(
                status=SaleStatusChoices.COMPLETED,
                created_at__gte=start_of_month,
                created_at__lte=now,
            ).count(),

            # Revenue sums
            'REVENUE_TODAY': Sale.objects.within_request_business(request).filter(
                status=SaleStatusChoices.COMPLETED,
                created_at__gte=start_of_today,
                created_at__lte=now,
            ).aggregate(_total_=models.Sum('total_price'))['_total_'] or 0,

            'REVENUE_TOTAL': Sale.objects.within_request_business(request).filter(
                status=SaleStatusChoices.COMPLETED
            ).aggregate(_total_=models.Sum('total_price'))['_total_'] or 0,
        }

    def run_calculations(self):
        self.indicators = Indicator.objects.within_request_business(self.request)
        for indicator in self.indicators:
            indicator.calculate_value(self.variables)
        return self.indicators
        