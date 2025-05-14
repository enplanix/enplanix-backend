from .base import *

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True


REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
    'rest_framework.authentication.SessionAuthentication'
]