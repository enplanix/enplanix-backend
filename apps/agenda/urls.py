from . import views

routes = [
    ('agendas', views.AgendaViewSet, 'agendas'),
]