import django_filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.sale.choices import SaleStatusChoices
from apps.sale.serializers import SaleSerializer, SaleItemSlimSerializer
from core.views import BusinessViewMixin
from .models import Sale, SaleItem
from rest_framework import filters
from rest_framework.exceptions import ValidationError


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


class SaleFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')


class SaleViewSet(ModelViewSet, BusinessViewMixin):
    model = Sale
    serializer_class = SaleSerializer
    search_fields = [
        'total_price', 
        'client__first_name', 
        'client__last_name', 
        'created_by__first_name', 
        'created_by__last_name'
    ]
    filterset_class = SaleFilter

    def get_serializer(self, *args, **kwargs):
        if self.action not in ['retrieve']:
            kwargs.update({'exclude': ['sale_items_read']})
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Sale.objects.within_request_business(self.request)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != SaleStatusChoices.PENDING:
            raise ValidationError('Não é possível alterar uma venda que não esteja pendente.')
        return super().update(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def get_sales_count(self, request):
        pending_count = self.get_queryset().filter(status=SaleStatusChoices.PENDING).count()
        return Response({
            'pending': pending_count 
        })

    @action(methods=['PATCH'], detail=True)
    def complete_sale(self, request, pk=None):
        instance = self.get_object()
        if instance.status != SaleStatusChoices.PENDING:
            raise ValidationError('Não é possível completar a venda, pois o status é diferente de Pendente.')
        if not instance.client:
            raise ValidationError('Não é possível completar uma venda sem cliente')
        if not instance.sale_items.exists():
            raise ValidationError('Não é possível completar uma venda sem itens')
            
        instance.status = SaleStatusChoices.COMPLETED
        instance.save()
        return Response({"detail": "Venda concluída"})

    @action(methods=['PATCH'], detail=True)
    def cancel_sale(self, request, pk=None):
        instance = self.get_object()    
        instance.status = SaleStatusChoices.CANCELED
        instance.save()
        return Response({"detail": "Venda cancelada"})
    
    def perform_create(self, serializer):
        instance = serializer.save(business=self.get_request_business(), created_by=self.request.user)
        instance.update_total_price()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.update_total_price()