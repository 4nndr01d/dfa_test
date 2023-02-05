from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from gallery_crud.pagination import PageNumberPagination
from pictures.models import Picture
from pictures.serializers import PictureSerializer


class PicturesViewSet(ModelViewSet):
    """
    Новости
    """
    pagination_class = PageNumberPagination
    serializer_class = PictureSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        if self.action == "delete_all":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Picture.objects.all()
        if self.request.user.is_authenticated:
            return Picture.objects.filter(user=self.request.user.id)
        return Picture.objects.none()

    @action(methods=['DELETE'], detail=False)
    def delete_all(self, request, *args, **kwargs):
        pictures = self.get_queryset()
        pictures.delete()
        return Response({"message": 'All pictures have been successfully deleted!'}, status=status.HTTP_204_NO_CONTENT)
