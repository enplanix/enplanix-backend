from django.core.management.base import BaseCommand
from ...models import Category, Subcategory

categories = {
    "Beleza e Cuidados Pessoais": {
        "PRODUCT": ["Cosméticos", "Produtos capilares", "Esmaltes", "Cremes hidratantes"],
        "SERVICE": ["Corte de cabelo", "Manicure e pedicure", "Maquiagem", "Escova e hidratação"]
    },
    "Pet Shop e Serviços para Animais": {
        "PRODUCT": ["Rações", "Brinquedos", "Higiene animal", "Acessórios para pet"],
        "SERVICE": ["Banho e tosa", "Consulta veterinária", "Adestramento", "Hospedagem pet"]
    },
    "Oficina Mecânica": {
        "PRODUCT": ["Peças e acessórios", "Óleo e lubrificantes", "Produtos de limpeza", "Baterias"],
        "SERVICE": ["Troca de óleo", "Mecânica geral", "Polimento e estética", "Alinhamento e balanceamento"]
    },
    "Informática e Tecnologia": {
        "PRODUCT": ["Computadores e periféricos", "Cabos e conectores", "Suprimentos de informática", "Acessórios gamer"],
        "SERVICE": ["Manutenção de PCs", "Formatação e backup", "Instalação de sistemas", "Suporte remoto"]
    },
    "Saúde e Bem-Estar": {
        "PRODUCT": ["Suplementos", "Equipamentos de uso pessoal", "Produtos naturais", "Óleos essenciais"],
        "SERVICE": ["Massoterapia", "Terapias alternativas", "Consultoria nutricional", "Acompanhamento fitness"]
    },
    "Esportes e Lazer": {
        "PRODUCT": ["Bicicletas", "Equipamentos de proteção", "Acessórios esportivos", "Roupas esportivas"],
        "SERVICE": ["Manutenção de bike", "Aulas de ciclismo", "Personal trainer", "Preparação física"]
    },
    "Design e Criatividade": {
        "PRODUCT": ["Impressões", "Produtos personalizados", "Quadros decorativos", "Material artístico"],
        "SERVICE": ["Design gráfico", "Fotografia", "Criação de identidade visual", "Edição de vídeo"]
    },
    "Cafeteria e Confeitaria": {
        "PRODUCT": ["Cafés especiais", "Doces artesanais", "Bolos caseiros", "Chás e infusões"],
        "SERVICE": ["Catering para eventos", "Cursos de barista", "Oficinas de confeitaria", "Degustações"]
    },
    "Moda e Costura": {
        "PRODUCT": ["Roupas sob medida", "Tecidos", "Acessórios de moda", "Kits de costura"],
        "SERVICE": ["Ajustes de roupa", "Criação sob medida", "Consultoria de estilo", "Cursos de costura"]
    },
    "Papelaria e Presentes": {
        "PRODUCT": ["Cadernos artesanais", "Canetas e lápis", "Adesivos", "Kits de scrapbooking"],
        "SERVICE": ["Encadernação personalizada", "Oficinas criativas", "Design de planners", "Cursos de caligrafia"]
    },
}


class Command(BaseCommand):
    help = 'Creates PRODUCT and SERVICE categories'

    def handle(self, *args, **kwargs):
        self.create_categories(categories)

    def create_categories(self, categorias_dict):
        for nome_categoria, tipos in categorias_dict.items():
            for tipo, subcats in tipos.items():
                categoria, _ = Category.objects.get_or_create(name=nome_categoria, type=tipo)
                for nome_subcat in subcats:
                    Subcategory.objects.get_or_create(name=nome_subcat, category=categoria)
