from django.urls import path
from rest_framework import routers

from .views import ProfileApi

router = routers.SimpleRouter()

router.register(r'profile', ProfileApi, 'profile')
profile_data = ProfileApi.as_view({'get': 'profile'})

urlpatterns = router.urls

urlpatterns += [
    path("profile/", profile_data, name='profile-data'),
]