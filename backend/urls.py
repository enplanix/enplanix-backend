from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import os

urlpatterns = [
    path('admin/', admin.site.urls),
]


# API URLS
urlpatterns += [
    path('api/', include('apps.urls')),
    # path('api/', include('apps.urls')),
    # path('api/access/', include('apps.access.urls')),
]