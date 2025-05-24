from rest_framework import viewsets
from rest_framework.decorators import action
from apps.agenda.models import Agenda
from rest_framework.response import Response

from apps.agenda.serializers import AgendaEditSerializer, AgendaPublicSerializer
from core.views import BusinessViewMixin

class AgendaViewSet(viewsets.ModelViewSet, BusinessViewMixin):
    def get_queryset(self):
        return Agenda.objects.within_request_business(self.request)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return AgendaEditSerializer
        return AgendaPublicSerializer
    
    def perform_create(self, serializer):
        serializer.save(business=self.get_request_business())

    @action(methods=['get'], detail=False)
    def get_by_date(self, request):
        date = request.query_params.get('date', None)
        if not date:
            return Response({'detail': 'Nenhuma data fornecida'})
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(date=date)
        serializer = AgendaPublicSerializer(queryset, many=True)
        return Response(serializer.data)
        