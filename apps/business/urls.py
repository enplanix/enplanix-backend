from . import views

routes = [
    ("members", views.BusinessMemberViewSet, "business_members"),
    ("business", views.BusinessViewSet, "business"),
]
