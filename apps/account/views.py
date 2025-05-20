from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.account.models import User
from apps.account.serializers import UserCreateSerializer


class UserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserCreateSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return super().get_permissions()