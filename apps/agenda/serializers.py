from rest_framework import serializers

from apps.agenda.models import Agenda


class AgendaEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        exclude = ['business']


class AgendaPublicSerializer(serializers.ModelSerializer):
    
    type = serializers.SerializerMethodField()

    class Meta:
        model = Agenda
        exclude = ['business']

    def get_type(self, instance):
        if hasattr(instance, 'extra'):
            return 'client'
        return 'basic'