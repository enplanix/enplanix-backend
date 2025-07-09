from apps.business.models import Business, Segment
from django.db import transaction

from apps.management.models import Category

DEFAULT_CATEGORIES = {
    1: [  # Serviços Diversos
        {"type": "SERVICE", "name": "Serviços Gerais"},
        {"type": "PRODUCT", "name": "Produtos Diversos"},
        {"type": "SERVICE", "name": "Consultoria e Suporte"}
    ],
    2: [  # Alimentação por Encomenda
        {"type": "SERVICE", "name": "Preparação de Refeições"},
        {"type": "PRODUCT", "name": "Alimentos Prontos"},
        {"type": "PRODUCT", "name": "Ingredientes e Insumos"}
    ],
    3: [  # Artesanato e Produtos Personalizados
        {"type": "SERVICE", "name": "Artesanato Personalizado"},
        {"type": "PRODUCT", "name": "Produtos Artesanais"},
        {"type": "PRODUCT", "name": "Materiais para Artesanato"}
    ],
    4: [  # Atividades Físicas e Saúde
        {"type": "SERVICE", "name": "Treinamento Físico"},
        {"type": "SERVICE", "name": "Consultoria Nutricional"},
        {"type": "PRODUCT", "name": "Equipamentos e Roupas Esportivas"},
        {"type": "PRODUCT", "name": "Suplementos Alimentares"}
    ],
    5: [  # Beleza e Estética
        {"type": "SERVICE", "name": "Cuidados de Beleza"},
        {"type": "SERVICE", "name": "Tratamentos Estéticos"},
        {"type": "PRODUCT", "name": "Cosméticos e Produtos de Beleza"}
    ],
    6: [  # Bem-estar e Terapias
        {"type": "SERVICE", "name": "Terapias e Bem-estar"},
        {"type": "PRODUCT", "name": "Produtos Naturais e Suplementos"},
        {"type": "SERVICE", "name": "Massagens e Relaxamento"}
    ],
    7: [  # Cabelereiro(a)
        {"type": "SERVICE", "name": "Serviços de Cabeleireiro"},
        {"type": "PRODUCT", "name": "Produtos para Cabelo"}
    ],
    8: [  # Consultoria e Serviços Profissionais
        {"type": "SERVICE", "name": "Consultorias Profissionais"},
        {"type": "PRODUCT", "name": "Materiais e Ferramentas"},
        {"type": "SERVICE", "name": "Planejamento Estratégico"}
    ],
    9: [  # Cuidados com Animais
        {"type": "SERVICE", "name": "Cuidados e Serviços para Animais"},
        {"type": "PRODUCT", "name": "Produtos para Animais"},
        {"type": "SERVICE", "name": "Adestramento e Treinamento"}
    ],
    10: [  # Educação e Treinamentos
        {"type": "SERVICE", "name": "Cursos e Treinamentos"},
        {"type": "PRODUCT", "name": "Materiais Educacionais"},
        {"type": "SERVICE", "name": "Aulas Particulares"}
    ],
    11: [  # Moda e Vestuário Sob Medida
        {"type": "SERVICE", "name": "Confecção Sob Medida"},
        {"type": "PRODUCT", "name": "Roupas e Acessórios"},
        {"type": "SERVICE", "name": "Ajustes e Reparos"}
    ],
    12: [  # Programação e Desenvolvimento
        {"type": "SERVICE", "name": "Desenvolvimento de Sistemas"},
        {"type": "PRODUCT", "name": "Softwares e Aplicativos"},
        {"type": "SERVICE", "name": "Consultoria em TI"}
    ],
    13: [  # Suporte Técnico e Instalações
        {"type": "SERVICE", "name": "Suporte Técnico"},
        {"type": "PRODUCT", "name": "Equipamentos e Peças"},
        {"type": "SERVICE", "name": "Instalações e Configurações"}
    ]
}


def create_default_categories(business):
    segment = business.segment
    for category in DEFAULT_CATEGORIES[segment.code]:
        Category.objects.create(**category, business=business)
