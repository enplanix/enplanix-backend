from apps.access.models import AccessPreference, UserPreference
from rest_framework import serializers

from django.contrib.auth import get_user_model

from apps.upload.serializers import ImageUploadPublicSerializer

User = get_user_model()


class UserPreferenceSerializer(serializers.ModelSerializer):

    avatar_data = ImageUploadPublicSerializer(source='avatar', read_only=True)

    class Meta:
        model = UserPreference
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    profile_preference = UserPreferenceSerializer(read_only=True)
    profile_preference_nested = UserPreferenceSerializer(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'full_name', 'profile_preference', 'profile_preference_nested']

    def get_full_name(self, instance):
        return f'{instance.first_name} {instance.last_name}'

    def create(self, validated_data):
        profile_preference_data = validated_data.pop('profile_preference_nested', None)
        user = super().create(validated_data)
        if profile_preference_data:
            preference, _ = UserPreference.objects.update_or_create(user=user, defaults=profile_preference_data)
            user.profile_preference = preference
        return user

    def update(self, instance, validated_data):
        profile_preference_data = validated_data.pop('profile_preference_nested', None)
        instance = super().update(instance, validated_data)
        if profile_preference_data and instance.profile_preference:
            instance.profile_preference = UserPreferenceSerializer().update(instance.profile_preference, profile_preference_data)
        return instance


class AccessPreferenceSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AccessPreference
        fields = '__all__'
