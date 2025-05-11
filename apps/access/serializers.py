from apps.access.models import AccessPreference
from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "phone", "first_name", "last_name", "full_name"]

    def get_full_name(self, instance):
        return f'{instance.first_name} {instance.last_name}'

class AccessPreferenceSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AccessPreference
        fields = "__all__"
