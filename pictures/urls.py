from rest_framework import routers

from pictures.views import PicturesViewSet

router = routers.SimpleRouter()

router.register(r'pictures', PicturesViewSet, 'pictures')

urlpatterns = router.urls
