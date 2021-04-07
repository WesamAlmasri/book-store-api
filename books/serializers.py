from rest_framework.serializers import Serializer, ModelSerializer
from .models import Category, Book

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
