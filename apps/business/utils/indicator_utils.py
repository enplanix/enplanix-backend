from apps.business.models import Indicator

DEFAULT_INDICATORS = [
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


def create_default_indicators(business):
    for indicator_data in DEFAULT_INDICATORS:
        Indicator.objects.create(
            business=business,
            **indicator_data
        )
