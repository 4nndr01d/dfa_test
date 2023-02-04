from django.urls import path, include
from .views import RegisterApi

urlpatterns = [
    path('registration/', RegisterApi.as_view()),
]
