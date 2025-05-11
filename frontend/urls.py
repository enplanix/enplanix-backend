from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^(?:.*)/?$', views.react_app),
    # path('', views.react_app)
]