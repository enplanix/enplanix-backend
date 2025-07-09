from sympy import sympify
from babel.numbers import format_decimal
from django.db import models
from django.utils import timezone

from apps.business.choices import IndicatorFormatChoices
from apps.business.models import Indicator


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
            IndicatorCalculator.recalculate_indicator_value(indicator, self.variables)
        return self.indicators
    
    @staticmethod
    def recalculate_indicator_value(indicator, variables):
        try:
            expr = sympify(indicator.formula)
            result = str(expr.subs(variables))
            match indicator.format:
                case IndicatorFormatChoices.INTEGER:
                    indicator.value = str(int(float(result)))
                case IndicatorFormatChoices.CURRENCY:
                    indicator.value = format_decimal(result, format='#,##0.00', locale='pt_BR')
                case _:
                    indicator.value = result
            indicator.save()
        except ZeroDivisionError:
            indicator.value = '0'
            indicator.save()
        except Exception as e:
            print("Error:", e)
            indicator.value = 'error'
            indicator.save()