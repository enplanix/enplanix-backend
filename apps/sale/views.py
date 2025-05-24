from rest_framework.viewsets import ModelViewSet

from apps.sale.serializers import SaleSerializer
from .models import Sale
import time

class SaleViewSet(ModelViewSet):
    model = Sale
    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.within_request_business(self.request)