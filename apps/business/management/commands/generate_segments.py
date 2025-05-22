from django.core.management.base import BaseCommand
from ...models import Segment

segments_data = [
        { "name": 'Serviços Diversos', "description": 'Serviços variados sob encomenda ou agendamento', "emoji": '🔧'},

        { "name": 'Barbearia', "description": 'Corte de cabelo e barba com atendimento por agendamento', "emoji": '💈' },
        { "name": 'Salão de Beleza', "description": 'Cabelo, unhas, maquiagem e estética com hora marcada', "emoji": '💅' },
        { "name": 'Manicure e Pedicure', "description": 'Serviços de unhas com atendimento em salão ou domicílio', "emoji": '💅' },
        { "name": 'Depiladora', "description": 'Depilação com cera, linha ou laser com agendamento', "emoji": '🪒' },
        { "name": 'Podóloga', "description": 'Cuidados com os pés e unhas com hora marcada', "emoji": '👣' },
        { "name": 'Maquiadora Profissional', "description": 'Maquiagem para eventos com agendamento', "emoji": '💄' },
        { "name": 'Designer de Sobrancelhas', "description": 'Modelagem e micropigmentação com hora marcada', "emoji": '👁️' },
        { "name": 'Esteticista', "description": 'Tratamentos faciais e corporais com agendamento', "emoji": '💆‍♀️' },
        { "name": 'Bronzeamento Artificial', "description": 'Sessões de bronze com horário agendado', "emoji": '🌞' },

        { "name": 'Psicólogo(a)', "description": 'Atendimento individual presencial ou online com hora marcada', "emoji": '🧠' },
        { "name": 'Nutricionista', "description": 'Consultas presenciais ou online com agendamento', "emoji": '🥗' },
        { "name": 'Fisioterapeuta', "description": 'Sessões de reabilitação com hora marcada', "emoji": '💪' },
        { "name": 'Massoterapeuta', "description": 'Massagens relaxantes ou terapêuticas com agendamento', "emoji": '💆‍♂️' },
        { "name": 'Terapeuta Holístico', "description": 'Reiki, aromaterapia e outras terapias com hora marcada', "emoji": '🕉️' },

        { "name": 'Pet Shop (Banho e Tosa)', "description": 'Serviços para pets com atendimento agendado', "emoji": '🐕' },
        { "name": 'Veterinário em domicílio', "description": 'Consultas e vacinas para animais com hora marcada', "emoji": '🐾' },
        { "name": 'Adestrador de cães', "description": 'Treinamentos personalizados com visitas agendadas', "emoji": '🐶' },

        { "name": 'Técnico em Informática', "description": 'Manutenção e suporte técnico com atendimento agendado', "emoji": '💻' },
        { "name": 'Assistência Técnica de Celulares', "description": 'Conserto de celulares com hora marcada', "emoji": '📱' },
        { "name": 'Instalador de Redes', "description": 'Configuração de redes Wi-Fi e cabeadas com visita agendada', "emoji": '🌐' },
        { "name": 'Técnico em CFTV', "description": 'Instalação de câmeras de segurança com horário marcado', "emoji": '📷' },

        { "name": 'Costureira', "description": 'Ajustes e roupas sob medida com agendamento', "emoji": '👗' },
        { "name": 'Alfaiate', "description": 'Confecção de roupas sociais com atendimento por hora marcada', "emoji": '👔' },
        { "name": 'Loja de Noivas', "description": 'Provas e atendimentos com hora marcada', "emoji": '👰' },

        { "name": 'Professor Particular', "description": 'Aulas de reforço ou idiomas com agendamento', "emoji": '👨‍🏫' },
        { "name": 'Instrutor de Pilates ou Yoga', "description": 'Aulas individuais ou em grupo com horário reservado', "emoji": '🧘‍♀️' },
        { "name": 'Personal Trainer', "description": 'Treinos personalizados com hora marcada', "emoji": '🏋️‍♀️' },

        { "name": 'Fotógrafo', "description": 'Ensaios e eventos com atendimento agendado', "emoji": '📸' },
        { "name": 'Videomaker/Editor de Vídeo', "description": 'Projetos audiovisuais com reuniões por agendamento', "emoji": '🎥' },
        { "name": 'Designer Gráfico', "description": 'Criação visual com briefing e entregas sob agendamento', "emoji": '🎨' },

        { "name": 'Consultor de Marketing Digital', "description": 'Atendimento estratégico com reuniões marcadas', "emoji": '📈' },
        { "name": 'Consultor de Tecnologia', "description": 'Ajuda técnica e escolha de equipamentos com agendamento', "emoji": '🖥️' },
        { "name": 'Consultor de Finanças Pessoais', "description": 'Planejamento financeiro com sessões por agendamento', "emoji": '💰' },

        { "name": 'Artesão sob encomenda', "description": 'Produtos personalizados feitos sob medida com prazo e consulta', "emoji": '🧶' },
        { "name": 'Ateliê de Costura Criativa', "description": 'Peças artesanais por encomenda e atendimento com hora marcada', "emoji": '🪡' },
        {
            "name": 'Loja de Presentes Personalizados',
            "description": 'Brindes e produtos feitos sob medida com retirada agendada',
            "emoji": '🎁',
        },

        { "name": 'Confeitaria por Encomenda', "description": 'Bolos e doces feitos sob agendamento e retirada programada', "emoji": '🍰' },
        { "name": 'Lanchonete Delivery', "description": 'Pedidos sob encomenda com horário de retirada ou entrega', "emoji": '🍔' },
        { "name": 'Padaria Artesanal', "description": 'Encomenda de pães, bolos e kits com retirada agendada', "emoji": '🥖' },
        { "name": 'Marmitaria Fit ou Caseira', "description": 'Refeições sob encomenda para retirada ou entrega programada', "emoji": '🍱' },
        { "name": 'Chef em Domicílio', "description": 'Cozinha exclusiva para eventos com atendimento sob agendamento', "emoji": '🍳' },
]




class Command(BaseCommand):
    help = 'Creates PRODUCT and SERVICE categories'

    def handle(self, *args, **kwargs):
        self.create_segments(segments_data)

    
    def create_segments(self, segments_data):
        for i, data in enumerate(segments_data):
            Segment.objects.get_or_create(code=i+1, defaults=data)


