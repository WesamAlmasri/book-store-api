from django.contrib import admin
from django.urls import path, include
from .views import LoginView

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

# router.register('login', LoginView)

urlpatterns = [
    path('', include(router.urls)),
    path('login', LoginView.as_view()),
]