from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.access.models import AccessPreference
from apps.access.serializers import AccessPreferenceSerializer, UserSerializer
from apps.business.serializers import BusinessPublicSerializer
from rest_framework import exceptions


class TokenViewSet(GenericViewSet):
    queryset = False
    permission_classes = [permissions.AllowAny]

    def list(self, *args, **kwargs):
        return Response([])

    @action(detail=False, methods=["post"], serializer_class=TokenObtainPairSerializer)
    def obtain(self, request, *args, **kwargs):
        return TokenObtainPairView.as_view()(request._request)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=TokenRefreshSerializer,
    )
    def refresh(self, request, *args, **kwargs):
        return TokenRefreshView.as_view()(request._request)


class MyAccessViewSet(GenericViewSet):
    queryset = None
    permission_classes = [permissions.IsAuthenticated]

    def get_current_access(self, request):
        try:
            return AccessPreference.objects.get(user=request.user)
        except AccessPreference.DoesNotExist:
            return Response({"detail": "Access preference not found for this user."}, status=404)    

    def list(self, request):
        try:
            instance = AccessPreference.objects.get(user=request.user)
            serializer = AccessPreferenceSerializer(instance, many=False)
            return Response(serializer.data)
        except AccessPreference.DoesNotExist:
            return Response({"detail": "Access preference not found for this user."}, status=404)    

    @action(methods=["get"], detail=False)
    def get_current_business(self, request):
        try:
            access_preference = self.get_current_access(request)
            current_business = access_preference.current_business
            if not current_business:
                raise exceptions.NotFound()
            if not current_business.members.filter(user=request.user):
                current_business = None
                access_preference.current_business = None
                access_preference.save()
            serializer = BusinessPublicSerializer(current_business)
            return Response(serializer.data)
        except (AccessPreference.DoesNotExist, exceptions.NotFound):
            return Response({"detail": "Business or access preference not found for this user."}, status=404)

    @action(methods=["patch"], detail=False)
    def update_config(self, request):
        access = self.get_current_access(request)
        serializer = AccessPreferenceSerializer(access, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=["patch"], detail=False, serializer_class=UserSerializer)
    def update_user_preferences(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)