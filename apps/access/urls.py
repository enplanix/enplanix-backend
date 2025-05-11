from . import views


routes = [
    ('me', views.MyAccessViewSet, 'me'),
    ('token', views.TokenViewSet, 'token'),
]