from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.sale.choices import SaleStatusChoices
from apps.sale.serializers import SaleSerializer, SaleItemSlimSerializer
from core.views import BusinessViewMixin
from .models import Sale, SaleItem


class SaleItemViewSet(ModelViewSet, BusinessViewMixin):
    serializer_class = SaleItemSlimSerializer

    def get_queryset(self):
        return SaleItem.objects.within_request_business(self.request).select_related('origin')

    def filter_queryset(self, queryset):
        sale = self.request.query_params.get('sale', None)
        queryset = super().filter_queryset(queryset)
        if sale:
            queryset = queryset.filter(sale=sale)
        return queryset


class SaleViewSet(ModelViewSet, BusinessViewMixin):
    model = Sale
    serializer_class = SaleSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action not in ['retrieve']:
            kwargs.update({'exclude': ['sale_items_read']})
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Sale.objects.within_request_business(self.request)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def get_sales_count(self, request):
        pending_count = self.get_queryset().filter(status=SaleStatusChoices.PENDING).count()
        return Response({
            'pending': pending_count 
        })

    def perform_create(self, serializer):
        instance = serializer.save(business=self.get_request_business(), created_by=self.request.user)
        instance.update_total_price()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.update_total_price()