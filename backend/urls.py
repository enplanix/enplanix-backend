from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
]


# API URLS
urlpatterns += [
    path('api/', include('apps.urls')),
    # path('api/', include('apps.urls')),
    # path('api/access/', include('apps.access.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()