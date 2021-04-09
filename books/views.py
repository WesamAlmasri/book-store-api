from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from .models import Category, Auther, Book, BookImage, BookComment
from user.models import CustomUser
from .serializers import CategorySerializer, AutherSerializer, BookSerializer, BookImageSerializer, BookCommentSerializer
from user.utils import get_query
from book_store.custom_methods import IsAuthenticatedCustom

class CategoryView(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        data = self.serializer_class(categories, many=True).data
        
        return Response(data, 200)

class AutherView(ModelViewSet):
    queryset = Auther.objects.all()
    serializer_class = AutherSerializer

    def get_permissions(self):
        if self.action == 'update' or 'create' or 'destroy':
            permission_classes = (IsAuthenticatedCustom,)
        else:
            permission_classes = ()

        return [permission() for permission in permission_classes] 

    def create(self, request):
        user = request.user

        if user and user.is_authenticated:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            auther = Auther.objects.create(user_id=user.id, name=serializer.validated_data['name'])
            return Response(self.serializer_class(auther).data, status=201)
        
        return Response({'error': 'You are not authorized to perform this operation'}, status=401)
    
    def update(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except:
            pass

        instance = self.get_object()
        
        user = request.user
        
        if user and user.is_authenticated and instance.user.id == user.id:
            serializer = self.serializer_class(data=request.data, instance=instance, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=200)

        return Response({'error': 'You are not authorized to perform this operation'}, status=401)
        


class BookView(ModelViewSet):
    queryset = Book.objects.all()
     