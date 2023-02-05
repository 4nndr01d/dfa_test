from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

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

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Picture.objects.all()
        if self.request.user.is_authenticated:
            return Picture.objects.filter(user=self.request.user.id)
        return Picture.objects.none()
