from email.policy import default
from rest_framework import serializers

from apps.upload.serializers import ImageUploadPublicSerializer
from .models import Category, Client, Product, Service


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


class CategorySerializer(serializers.ModelSerializer):

    ref_count = serializers.IntegerField(default=0, read_only=True) # annotated

    class Meta:
        model = Category
        fields = '__all__'

    