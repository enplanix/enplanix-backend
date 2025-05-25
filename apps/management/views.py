from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.db.models import Count
from core.views import BusinessViewMixin

from .serializers import CategorySerializer, ClientSerializer, ProductEditSerializer, ProductPublicSerializer, ServiceEditSerializer, ServicePublicSerializer
from .models import Category, Client, OfferType, Product, Service


class ClientViewSet(ModelViewSet, BusinessViewMixin):
    serializer_class = ClientSerializer
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'address']

    def get_queryset(self):
        return Client.objects.within_request_business(self.request)

    def perform_create(self, serializer):
        serializer.save(business=self.get_request_business())


class ProductViewSet(ModelViewSet, BusinessViewMixin):
    search_fields = ['name', 'code']

    def get_queryset(self):
        return Product.objects.within_request_business(self.request)
        
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ProductEditSerializer
        return ProductPublicSerializer

    def perform_create(self, serializer):
        serializer.save(business=self.get_request_business())

    @action(methods=['get'], detail=False)
    def get_categories(self, request):
        queryset = Category.objects.filter(type=OfferType.PRODUCT)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False, permission_classes=[permissions.AllowAny])
    def get_public_products(self, request):
        business = request.query_params.get('business', None)
        if not business:
            return Response({'detail': 'Business not specified'}, status=400)
        queryset = self.filter_queryset(Product.objects.within_request_business(self.request))
        serializer = ProductPublicSerializer(queryset, many=True)
        return Response(serializer.data)


class ServiceViewSet(ModelViewSet):
    search_fields = ['name', 'code']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ServiceEditSerializer
        return ServicePublicSerializer

    def get_queryset(self):
        return Service.objects.within_request_business(self.request)
    
    def perform_create(self, serializer):
        serializer.save(business=self.request.user.preference.current_business)

    @action(methods=['get'], detail=False)
    def get_categories(self, request):
        queryset = Category.objects.filter(type=OfferType.SERVICE)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False, permission_classes=[permissions.AllowAny])
    def get_public_services(self, request):
        business = request.query_params.get('business', None)
        if not business:
            return Response({'detail': 'Business not specified'}, status=400)
        queryset = self.filter_queryset(Service.objects.within_request_business(self.request))
        serializer = ServicePublicSerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(ModelViewSet, BusinessViewMixin):
    serializer_class = CategorySerializer
    search_fields = ['name']

    def get_queryset(self):
        return Category.objects.within_request_business(self.request)

    def filter_queryset(self, queryset):
        category_type = self.request.query_params.get('type', None)
        include_count = self.request.query_params.get('include_count', None)
        queryset =  super().filter_queryset(queryset)
        if category_type:
            queryset = queryset.filter(type=category_type)
        if include_count:
            queryset = queryset.annotate(ref_count=Count('offer'))
        return queryset

    def perform_create(self, serializer):
        serializer.save(business=self.get_request_business())

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError('Não foi possível excluir esta categoria, pois ela está vinculada a um ou mais produtos ou serviços.')