from email.policy import default
from rest_framework import serializers
from .models import FileUpload, ImageUpload
from django.urls import reverse

class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileUpload
        fields = '__all__'

class FileUploadPublicSerializer(serializers.ModelSerializer):
    uploaded = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = FileUpload
        fields = ['id', 'name', 'uploaded']


class ImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageUpload
        fields = '__all__'

class ImageUploadPublicSerializer(serializers.ModelSerializer):
    
    uploaded = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = ImageUpload
        fields = ['id', 'name', 'uploaded']
