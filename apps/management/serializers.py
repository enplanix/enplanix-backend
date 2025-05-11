from rest_framework import serializers

from apps.upload.serializers import ImageUploadPublicSerializer, ImageUploadSerializer
from .models import Category, Client, Product, Service, Subcategory


class ClientSerializer(serializers.ModelSerializer):
    
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        exclude = ['business']

    def get_full_name(self, instance):
        return f'{instance.first_name} {instance.last_name}'.strip()


class ProductEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['business']


class ProductPublicSerializer(serializers.ModelSerializer):
    cover = ImageUploadPublicSerializer(read_only=True)
    category_display = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        exclude = ['business']


class ServiceEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ['business']


class ServicePublicSerializer(serializers.ModelSerializer):
    cover = ImageUploadPublicSerializer(read_only=True)
    category_display = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Service
        exclude = ['business']


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_subcategories(self, instance):
        return SubCategorySerializer(instance.subcategories.all(), many=True).data
