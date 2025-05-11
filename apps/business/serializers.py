from rest_framework import serializers

from apps.access.serializers import UserSerializer
from apps.business.models import Business, BusinessMember, Segment, SegmentCategory
from apps.upload.serializers import ImageUploadPublicSerializer, ImageUploadSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class BusinessPublicSerializer(serializers.ModelSerializer):
    cover = ImageUploadPublicSerializer(read_only=True)
    logo = ImageUploadPublicSerializer(read_only=True)
    category = serializers.CharField(source='segment.category.id') 

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
        

class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = '__all__'


class SegmentCategorySerializer(serializers.ModelSerializer):
    segments = serializers.SerializerMethodField()

    class Meta:
        model = SegmentCategory
        fields = '__all__'

    def get_segments(self, instance):
        return SegmentSerializer(instance.segments.all(), many=True).data
