
from PIL import Image
from django.db.models import signals
from django.dispatch import receiver

from apps.business.models import BusinessMember, BusinessConfig, Indicator
from apps.upload.models import ImageUpload
from core.context import current_request


def create_default_indicators(business):
    default_indicators = [
        {
            'name': 'Vendas hoje',
            'formula': 'SALES_COMPLETED_TODAY_COUNT',
            'description': 'Total de vendas concluídas hoje.',
            'format': 'INTEGER',
        },
        {
            'name': 'Faturamento hoje',
            'formula': 'REVENUE_TODAY',
            'description': 'Faturamento total obtido hoje.',
            'format': 'CURRENCY',
        },
        {
            'name': 'Agendamentos hoje',
            'formula': 'AGENDAS_TODAY_COUNT',
            'description': 'Total de agendamentos marcados para hoje.',
            'format': 'INTEGER',
        },
        {
            'name': 'Clientes ativos',
            'formula': 'CLIENTS_COUNT',
            'description': 'Quantidade de clientes cadastrados.',
            'format': 'INTEGER',
        },
        {
            'name': 'Produtos cadastrados',
            'formula': 'PRODUCTS_COUNT',
            'description': 'Total de produtos disponíveis.',
            'format': 'INTEGER',
        },
        {
            'name': 'Serviços disponíveis',
            'formula': 'SERVICES_COUNT',
            'description': 'Total de serviços oferecidos.',
            'format': 'INTEGER',
        },
        {
            'name': 'Vendas no mês',
            'formula': 'SALES_COMPLETED_MONTH_COUNT',
            'description': 'Vendas concluídas no mês atual.',
            'format': 'INTEGER',
        },
        {
            'name': 'Receita total',
            'formula': 'REVENUE_TOTAL',
            'description': 'Faturamento total acumulado.',
            'format': 'CURRENCY',
        },
    ]

    for indicator_data in default_indicators:
        Indicator.objects.create(
            business=business,
            **indicator_data
        )


@receiver(signals.post_save, sender='business.Business')
def set_additional_business_models(instance, created=False, **kwargs): 
    request = current_request.get()
    if created:
        BusinessMember.objects.create(business=instance, user=request.user)
        BusinessConfig.objects.get_or_create(business=instance)
        create_default_indicators(instance)


@receiver(signals.post_delete, sender='business.Business')
def remove_business_images(instance, **kwargs):
    ImageUpload.objects.filter(id__in=[instance.cover_id, instance.logo_id]).delete()