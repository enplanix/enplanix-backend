from . import views

routes = [
    ("sale_items", views.SaleItemViewSet, "sale_items"),
    ("sales", views.SaleViewSet, "sales"),
]
