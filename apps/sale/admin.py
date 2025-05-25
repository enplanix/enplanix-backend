from django.contrib import admin
from .models import Sale, SaleItem 



class SaleItemInline(admin.TabularInline):
    model = SaleItem
    exclude = ['type']
    readonly_fields = ['snapshot_name', 'snapshot_code', 'snapshot_price']
    extra = 1



@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = ['business', 'created_by', 'client', 'payment', 'status', 'total_price']
    readonly_fields = ['total_price']


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    # inlines = [ServiceSaleItemInline, ProductSaleItemInline]
    # readonly_fields = ['total_price']
    pass