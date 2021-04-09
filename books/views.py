from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from .models import Category, Auther
from .serializers import CategorySerializer, AutherSerializer, BookSerializer, BookImageSerializer, BookCommentSerializer
from user.utils import get_query

class CategoryView(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        data = self.serializer_class(categories, many=True).data
        
        return Response(data, 200)

class AutherView(ModelViewSet):
    queryset = Auther.objects.all()
    serializer_class = AutherSerializer


    