from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import CategorySerializer, ClientSerializer, ProductEditSerializer, ProductPublicSerializer, ServiceEditSerializer, ServicePublicSerializer
from .models import Category, Client, OfferType, Product, Service

class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'address']

    def get_queryset(self):
        business = self.request.user.preference.current_business
        if business:
            return Client.objects.filter(business=business)
        return Client.objects.none()

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.preference.current_business)


class ProductViewSet(ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ProductEditSerializer
        return ProductPublicSerializer

    def get_queryset(self):
        business = self.request.user.preference.current_business
        if business:
            return Product.objects.filter(business=business)
        return Product.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(business=self.request.user.preference.current_business)

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
        queryset = self.filter_queryset(Product.objects.filter(business=business))
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
        business = self.request.user.preference.current_business
        if business:
            return Service.objects.filter(business=business)
        return Service.objects.none()
    
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
        queryset = self.filter_queryset(Service.objects.filter(business=business))
        serializer = ServicePublicSerializer(queryset, many=True)
        return Response(serializer.data)