from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.business.models import Business, BusinessConfig, BusinessMember, Segment
from apps.business.serializers import BusinessConfigSerializer, BusinessEditSerializer, BusinessMembeAddSerializer, BusinessMemberPublicSerializer, BusinessPublicSerializer, SegmentSerializer
from rest_framework import filters
import time

class BusinessViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BusinessEditSerializer
        return BusinessPublicSerializer

    def get_queryset(self):
        user = self.request.user
        if user:
            return Business.objects.filter(members__user=user)
        return Business.objects.none()

    def perform_create(self, serializer):
        serializer.save()

    @action(methods=['get'], detail=False)
    def get_segments(self, request):
        categories_data = Segment.objects.all()
        serializer = SegmentSerializer(categories_data, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def add_member(self, request):
        serializer = BusinessMembeAddSerializer(data=request.data, business=self.request.user.preference.current_business)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Sucesso"})


class BusinessMemberViewSet(ModelViewSet):
    serializer_class = BusinessMemberPublicSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__email', 'user__first_name', 'user__last_name']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BusinessMembeAddSerializer
        return BusinessMemberPublicSerializer

    def get_queryset(self):
        business = self.request.user.preference.current_business
        if business:
            return BusinessMember.objects.filter(business=business)
        return BusinessMember.objects.none()


class BusinessConfigViewSet(ModelViewSet):
    serializer_class = BusinessConfigSerializer
    model = BusinessConfig
    
    def get_queryset(self):
        business = self.request.user.preference.current_business
        if business:
            return BusinessConfig.objects.filter(business=business)
        return BusinessConfig.objects.none()

    @action(methods=['get'], detail=False)
    def get_current(self, request):
        instance = self.filter_queryset(self.get_queryset()).first()
        serializer = BusinessConfigSerializer(instance)
        return Response(serializer.data)