from rest_framework import serializers

from apps.access.serializers import UserSerializer
from apps.business.models import Business, BusinessConfig, BusinessMember, Segment
from apps.upload.serializers import ImageUploadPublicSerializer, ImageUploadSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
from rest_framework.exceptions import ValidationError

User = get_user_model()

class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = '__all__'


class BusinessConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessConfig
        exclude = ['business']
    
    def validate(self, attrs):
        start = datetime.combine(timezone.now().date(), attrs['agenda_start_time'])
        end = datetime.combine(timezone.now().date(), attrs['agenda_end_time'])
        # total_diff = (end - start).seconds / 3600
        # min_diff = 2
        if start >= end:
            raise ValidationError("Horário de início não deve ser maior que horário de fim.")
        return super().validate(attrs)


class BusinessPublicSerializer(serializers.ModelSerializer):
    cover = ImageUploadPublicSerializer(read_only=True)
    logo = ImageUploadPublicSerializer(read_only=True)
    config = BusinessConfigSerializer(read_only=True)
    segment_data = SegmentSerializer(source='segment', read_only=True) 
    
    class Meta:
        model = Business
        fields = '__all__'


class BusinessEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)


class BusinessMemberPublicSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BusinessMember
        fields = '__all__'


class BusinessMembeAddSerializer(serializers.Serializer):

    class Meta:
        model = BusinessMember
        fields = '__all__'


class BusinessMembeAddSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def __init__(self, *args, business=None, **kwargs):
        self.user = None
        self.business = business
        self.instance = None
        super().__init__(*args, **kwargs)

    def validate(self, validated_data):
        if not self.business:
            raise serializers.ValidationError('Negócio não encontrado')
        email = validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'O email não está cadastrado em nossa plataforma.'})
        self.user = user
        return validated_data
    
    def create(self, validated_data):
        instance = BusinessMember.objects.get_or_create(user=self.user, business=self.business)
        return instance
