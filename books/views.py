from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from .models import Category, Auther, Book, BookImage, BookComment
from user.models import CustomUser, FileUpload
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
        if self.action == 'update' or 'create' or 'destroy' or 'partial_update':
            permission_classes = (IsAuthenticatedCustom,)
        else:
            permission_classes = ()

        return [permission() for permission in permission_classes]

    def create(self, request):
        user = request.user

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auther = Auther.objects.create(
            user_id=user.id, name=serializer.validated_data['name'])
        return Response(self.serializer_class(auther).data, status=201)

    def update(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except:
            pass

        instance = self.get_object()

        user = request.user

        if instance.user.id == user.id:
            serializer = self.serializer_class(
                data=request.data, instance=instance, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=200)

        return Response({'error': 'You are not authorized to perform this operation'}, status=401)


class BookView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action == 'update' or 'create' or 'destroy' or 'partial_update':
            permission_classes = (IsAuthenticatedCustom,)
        else:
            permission_classes = ()

        return [permission() for permission in permission_classes]

    def get_queryset(self):

        if self.request.method.lower() != 'get':
            return self.queryset

        data = self.request.query_params.dict()
        data.pop('page', None)
        keyword = data.pop('keyword', None)

        if keyword:
            search_fields = ('auther__name', 'category__name',
                             'title', 'description')
            query = get_query(keyword, search_fields)

            try:
                return self.queryset.filter(query).filter(**data).distinct()
            except Exception as e:
                raise Exception(e)

        return self.queryset.filter(**data).distinct()

    def create(self, request):
        user = request.user

        if not user.user_auther:
            return Response({"error": "You have to make an auther account to upload books!"}, status=400)

        serializer = self.serializer_class(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['auther_id'] != user.user_auther.id:
            return Response({"error": "Something Went Wrong"}, status=400)

        serializer.save()
        return Response(serializer.data, status=200)


    def update(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except:
            pass

        user = request.user

        if not user.user_auther:
            return Response({"error": "You have to make an auther account to upload books!"}, status=400)

        instance = self.get_object()

        try:
            serializer = self.serializer_class(
                data=request.data, instance=instance, partial=True)
            serializer.is_valid(raise_exception=True)

            if serializer.validated_data['auther_id'] != user.auther_user.id:
                return Response({"error": "You do not own the book to update on!"}, status=400)

            serializer.save()
            return Response(serializer.data, status=200)
        except Exception:
            return Response({"error": "failed to upload the book"}, status=400)

        return Response(serializer.data, status=200)
