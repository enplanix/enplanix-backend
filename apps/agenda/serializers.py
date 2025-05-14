from rest_framework import serializers

from apps.agenda.models import Agenda, AgendaExtra

class AgendaExtraSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgendaExtra
        fields = '__all__'

class AgendaEditSerializer(serializers.ModelSerializer):
    
    extra_nested = AgendaExtraSerializer(write_only=True, required=False)
    
    class Meta:
        model = Agenda
        exclude = ['business']
    
    def create(self, validated_data):
        extra_data = validated_data.pop('extra_nested', None)
        agenda = super().create(validated_data)
        if extra_data:
            extra, _ = AgendaExtra.objects.update_or_create(agenda=agenda, defaults=extra_data)
            agenda.extra = extra
        return agenda

    def update(self, instance, validated_data):
        extra_data = validated_data.pop('extra_nested', None)
        instance = super().update(instance, validated_data)
        if extra_data and instance.extra:
            instance.extra = AgendaExtraSerializer().update(instance.extra, extra_data)
        return instance

class AgendaPublicSerializer(serializers.ModelSerializer):
    
    type = serializers.SerializerMethodField()
    extra_nested = AgendaExtraSerializer(source='extra', read_only=True)

    class Meta:
        model = Agenda
        exclude = ['business']

    def get_type(self, instance):
        if hasattr(instance, 'extra'):
            return 'client'
        return 'basic'
