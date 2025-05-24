from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from core.views import BusinessViewMixin

from .serializers import CategorySerializer, ClientSerializer, ProductEditSerializer, ProductPublicSerializer, ServiceEditSerializer, ServicePublicSerializer
from .models import Category, Client, OfferType, Product, Service


class ClientViewSet(ModelViewSet, BusinessViewMixin):
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'address']

    def get_queryset(self):
        return Client.objects.within_request_business(self.request)

    def perform_create(self, serializer):
        serializer.save(business=self.get_request_business())


class ProductViewSet(ModelViewSet, BusinessViewMixin):
    filter_backends = [filters.SearchFilter]
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
    filter_backends = [filters.SearchFilter]
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


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        category_type = self.request.query_params.get('type', None)
        if not category_type:
            return Category.objects.none()
        return Category.objects.within_request_business(self.request).filter(type=category_type)