from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.business.models import Business, BusinessConfig, BusinessMember, Indicator, IndicatorCalculator, Segment
from apps.business.serializers import BusinessConfigSerializer, BusinessEditSerializer, BusinessMembeAddSerializer, BusinessMemberPublicSerializer, BusinessDetailSerializer, BusinessPublicSerializer, IndicatorSerializer, SegmentSerializer
from rest_framework import filters, permissions
from rest_framework import mixins
from core.utils import observe_queries
from core.views import BusinessViewMixin


class CustomBusinessFilter(filters.SearchFilter):

    def get_search_fields(self, view, request):
        if view.action == 'get_segments':
            return ['name', 'code', 'description']
        return super().get_search_fields(view, request)


class BusinessViewSet(ModelViewSet, BusinessViewMixin):
    filter_backends = [CustomBusinessFilter]
    
    def get_queryset(self):
        return Business.objects.from_request_user(self.request)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BusinessEditSerializer
        return BusinessDetailSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

    @action(methods=['get'], detail=False)
    def get_segments(self, request):
        page = self.paginate_queryset(self.filter_queryset(Segment.objects.all()))
        serializer = SegmentSerializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return response

    @action(methods=['post'], detail=False)
    def add_member(self, request):
        serializer = BusinessMembeAddSerializer(data=request.data, business=self.get_request_business())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Sucesso"})


class BusinessMemberViewSet(ModelViewSet, BusinessViewMixin):
    serializer_class = BusinessMemberPublicSerializer
    search_fields = ['user__email', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        return BusinessMember.objects.within_request_business(self.request).select_related('user__profile_preference')

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BusinessMembeAddSerializer
        return BusinessMemberPublicSerializer


class BusinessConfigViewSet(ModelViewSet, BusinessViewMixin):
    serializer_class = BusinessConfigSerializer
    model = BusinessConfig
    
    def get_queryset(self):
        return BusinessConfig.objects.within_request_business(self.request)

    @action(methods=['get'], detail=False)
    def get_current(self, request):
        instance = self.filter_queryset(self.get_queryset()).first()
        serializer = BusinessConfigSerializer(instance)
        return Response(serializer.data)


class IndicatorViewSet(ModelViewSet):
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()

    def get_queryset(self):
        return IndicatorCalculator(self.request).run_calculations()


class CatalogViewSet(GenericViewSet):
    permission_classes = [permissions.AllowAny]
    
    @action(methods=['get'], detail=False)
    def get_business_by_slug(self, request):
        slug = request.query_params.get('slug', '')
        if not slug:
            return Response({"detail": "Slug not provided"}, status=404)
        business = get_object_or_404(Business, slug=slug)
        serializer = BusinessPublicSerializer(business)
        return Response(serializer.data)
