from rest_framework.viewsets import ModelViewSet

from apps.sale.serializers import SaleSerializer
from .models import Sale
import time

class SaleViewSet(ModelViewSet):
    model = Sale
    serializer_class = SaleSerializer

    def get_queryset(self):
        business = self.request.user.preference.current_business
        if business:
            return Sale.objects.filter(business=business)
        return Sale.objects.none()