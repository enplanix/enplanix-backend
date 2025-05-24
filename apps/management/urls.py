from . import views

routes = [
    ('clients', views.ClientViewSet, 'clients'),
    ('products', views.ProductViewSet, 'products'),
    ('services', views.ServiceViewSet, 'services'),
    ('categories', views.CategoryViewSet, 'categories'),
]