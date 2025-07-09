from apps.business.models import Business, Segment
from django.db import transaction

DEFAULT_SEGMENTS = [
    {
        "code": 1,
        "name": "Serviços Diversos",
        "description": "Serviços variados sob encomenda ou agendamento.",
        "emoji": "🔧"
    },
    {
        "code": 2,
        "name": "Alimentação por Encomenda",
        "description": "Comidas, bolos, marmitas e outros alimentos sob demanda.",
        "emoji": "🍱"
    },
    {
        "code": 3,
        "name": "Artesanato e Produtos Personalizados",
        "description": "Produtos feitos à mão, lembranças, presentes e personalizados.",
        "emoji": "🎁"
    },
    {
        "code": 4,
        "name": "Atividades Físicas e Saúde",
        "description": "Serviços de treinamento, nutrição e práticas corporais.",
        "emoji": "💪"
    },
    {
        "code": 5,
        "name": "Beleza e Estética",
        "description": "Serviços de cuidados pessoais como unhas, maquiagem, cabelo e estética.",
        "emoji": "💅"
    },
    {
        "code": 6,
        "name": "Bem-estar e Terapias",
        "description": "Terapias físicas, emocionais e alternativas com agendamento.",
        "emoji": "🧘‍♀️"
    },
    {
        "code": 7,
        "name": "Cabelereiro(a)",
        "description": "Corte, coloração, escova e tratamentos capilares com agendamento.",
        "emoji": "💇‍♀️"
    },
    {
        "code": 8,
        "name": "Consultoria e Serviços Profissionais",
        "description": "Consultoria em finanças, marketing, tecnologia e planejamento.",
        "emoji": "📊"
    },
    {
        "code": 9,
        "name": "Cuidados com Animais",
        "description": "Banho, tosa, consultas veterinárias e adestramento.",
        "emoji": "🐾"
    },
    {
        "code": 10,
        "name": "Educação e Treinamentos",
        "description": "Aulas particulares, reforço escolar e treinamento de animais.",
        "emoji": "👨‍🏫"
    },
    {
        "code": 11,
        "name": "Moda e Vestuário Sob Medida",
        "description": "Costura, ajustes, confecção e roupas personalizadas.",
        "emoji": "🧵"
    },
    {
        "code": 12,
        "name": "Programação e Desenvolvimento",
        "description": "Desenvolvimento de sites, sistemas, apps e automações.",
        "emoji": "💻"
    },
    {
        "code": 13,
        "name": "Suporte Técnico e Instalações",
        "description": "Serviços técnicos, manutenção, redes e segurança eletrônica.",
        "emoji": "🛠️"
    }
]


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


def create_default_segments():
    with transaction.atomic():
        Segment.objects.all().delete()
        for segment in DEFAULT_SEGMENTS:
            Segment.objects.create(**segment)
        
        default_segment = Segment.objects.get(code=1)
        Business.objects.update(segment=default_segment)