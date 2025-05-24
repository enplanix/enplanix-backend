from rest_framework import serializers

from apps.access.serializers import UserSerializer
from apps.management.serializers import ClientSerializer
from .models import Sale


class SaleSerializer(serializers.ModelSerializer):

    user_data = UserSerializer(source='created_by', read_only=True)
    client_data = ClientSerializer(source='client', read_only=True)

    class Meta:
        model = Sale
        exclude = ['business', 'created_by']