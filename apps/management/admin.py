from django.contrib import admin
# from .models import Category, Client, Service, Product, CategoryTemplate
from .models import Client, Service, Product, Category, CategoryTemplate, CategoryTemplate


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'duration']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(CategoryTemplate)
class CategoryTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'segment']
    list_filter = ['type', 'segment']
    list_editable = ['segment']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    list_filter = ['type']
