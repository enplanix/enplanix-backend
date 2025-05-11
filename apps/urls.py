from rest_framework.routers import DefaultRouter
from django.urls import path, include
from importlib import import_module

router = DefaultRouter()

def register_routes(router, routes, prefix):
    for route, viewset, basename in routes:
        path_name = f'{prefix}/{route}' if route != prefix else route
        router.register(path_name, viewset, basename)

register_routes(router, import_module("apps.account.urls").routes, 'account')
register_routes(router, import_module("apps.access.urls").routes, 'access')
register_routes(router, import_module("apps.business.urls").routes, 'business')
register_routes(router, import_module("apps.upload.urls").routes, 'upload')
register_routes(router, import_module("apps.management.urls").routes, 'management')
register_routes(router, import_module("apps.agenda.urls").routes, 'agenda')


urlpatterns = [
    path('', include(router.urls))
]