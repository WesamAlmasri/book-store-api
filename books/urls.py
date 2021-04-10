from django.urls import path, include
from .views import CategoryView, AutherView, BookView, BookImageView

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register('authers', AutherView)
router.register('book', BookView)
router.register('book-image', BookImageView)

urlpatterns = [
    path('', include(router.urls)),
    path('categories', CategoryView.as_view()),
]