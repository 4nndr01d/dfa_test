import rest_framework.status
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import ProfileSerializer, RegisterSerializer


class ProfileApi(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'registration':
            return RegisterSerializer
        return ProfileSerializer

    @method_decorator(decorator=swagger_auto_schema(responses={'201': ProfileSerializer(many=True)}))
    @action(methods=['POST'], detail=False, pagination_class=None)
    def registration(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(ProfileSerializer(user).data, status=rest_framework.status.HTTP_201_CREATED)

    def profile(self, request, *args, **kwargs):
        return Response(ProfileSerializer(self.request.user).data)
