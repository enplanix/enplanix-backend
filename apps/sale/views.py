from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.sale.serializers import SaleSerializer
from core.views import BusinessViewMixin
from .models import Sale

import time


class SaleViewSet(ModelViewSet, BusinessViewMixin):
    model = Sale
    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.within_request_business(self.request)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def get_sales_count(self, request):
        pending_count = self.get_queryset().filter(status=Sale.StatusChoices.PENDING).count()
        return Response({
            'pending': pending_count 
        })

    def perform_create(self, serializer):
        serializer.save(business=self.get_request_business(), created_by=self.request.user)