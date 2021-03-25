from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

# router.register(url, veiw)

urlpatterns = [
    path('', include(router.urls))
]