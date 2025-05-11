from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from .models import User

class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password']
    
    def validate_password(self, value):
        return make_password(value)