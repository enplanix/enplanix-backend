import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

# Define qual settings usar
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Carrega o app HTTP (Django)
django_asgi_app = get_asgi_application()

# Carrega as rotas WebSocket
from apps.ws.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

# Verifica se estamos em produção
IS_PROD = os.getenv("PROJECT_SETTINGS") == "prod"

if IS_PROD:
    websocket_application = AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    )
else:
    websocket_application = AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": websocket_application,
    }
)
