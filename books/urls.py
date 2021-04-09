from django.urls import path, include
from .views import CategoryView, AutherView, BookView

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register('authers', AutherView)
router.register('book', BookView)

urlpatterns = [
    path('', include(router.urls)),
    path('categories', CategoryView.as_view()),
]