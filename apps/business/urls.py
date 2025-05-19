from . import views

routes = [
    ("members", views.BusinessMemberViewSet, "business_members"),
    ("business_config", views.BusinessConfigViewSet, "business_config"),
    ("business", views.BusinessViewSet, "business"),
]
