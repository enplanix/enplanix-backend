from rest_framework import viewsets
from rest_framework.decorators import action
from apps.agenda.models import Agenda
from rest_framework.response import Response

from apps.agenda.serializers import AgendaEditSerializer, AgendaPublicSerializer

class AgendaViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return AgendaEditSerializer
        return AgendaPublicSerializer

    def get_current_business(self):
        return self.request.user.preference.current_business

    def get_queryset(self):
        business = self.get_current_business()
        if business:
            return Agenda.objects.filter(business=business)
        return Agenda.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(business=self.get_current_business())

    @action(methods=['get'], detail=False)
    def get_by_date(self, request):
        date = request.query_params.get('date', None)
        if not date:
            return Response({'detail': 'Nenhuma data fornecida'})
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(date=date)
        serializer = AgendaPublicSerializer(queryset, many=True)
        return Response(serializer.data)
        