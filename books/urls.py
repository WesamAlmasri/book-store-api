from django.urls import path, include
from .views import CategoryView, AutherView

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register('authers', AutherView)

urlpatterns = [
    path('', include(router.urls)),
    path('categories', CategoryView.as_view()),
]