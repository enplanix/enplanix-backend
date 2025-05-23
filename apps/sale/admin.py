from django.contrib import admin
from .models import Sale, ProductSaleItem, ServiceSaleItem


class ServiceSaleItemInline(admin.TabularInline):
    model = ServiceSaleItem
    exclude = ['type']
    readonly_fields = ['snapshot_name', 'snapshot_code', 'snapshot_price']
    extra = 1

class ProductSaleItemInline(admin.TabularInline):
    model = ProductSaleItem
    exclude = ['type']
    readonly_fields = ['snapshot_name', 'snapshot_code', 'snapshot_price']
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [ServiceSaleItemInline, ProductSaleItemInline]
    readonly_fields = ['total_price']