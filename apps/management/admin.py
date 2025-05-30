from django.contrib import admin
from .models import Client, Offer, Product, Service, Category, CategoryTemplate, CategoryTemplate


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'duration']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


# @admin.register(OfferV2)
# class OfferV2Admin(admin.ModelAdmin):
#     list_display = ['id', 'name']


# @admin.register(Service)
# class ServiceV2Admin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'price', 'duration']


# @admin.register(Product)
# class ProductV2Admin(admin.ModelAdmin):
#     list_display = ['id', 'name']


@admin.register(CategoryTemplate)
class CategoryTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'segment']
    list_filter = ['type', 'segment']
    list_editable = ['segment']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    list_filter = ['type', 'business']
