from django.http import FileResponse
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from apps.upload.models import FileUpload, ImageUpload
from apps.upload.serializers import FileUploadSerializer, ImageUploadPublicSerializer, ImageUploadSerializer
from rest_framework.decorators import action
from rest_framework import permissions


class FileUploadViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(methods=["get"], detail=True)
    def content(self, *_, **__):
        instance = self.get_object()
        return FileResponse(instance.file, as_attachment=False)


class ImageUploadViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = ImageUpload.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ImageUploadSerializer
        return ImageUploadPublicSerializer

    @action(methods=["get"], detail=True)
    def content(self, *_, **__):
        instance = self.get_object()
        return FileResponse(instance.file, as_attachment=False)

