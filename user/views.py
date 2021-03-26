from django.shortcuts import render
from .models import JWT, CustomUser, FileUpload, UserProfile
from .utils import JWTToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer, RefreshSerializer, FileUploadSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from .authentication import Authentication
from django.db.models import Q
import re
from book_store.custom_methods import IsAuthenticatedCustom


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if not user:
            return Response({"error": "Invalid Username or Password"}, status=400)
        
        JWT.objects.filter(user_id=user.id).delete()

        access = JWTToken.get_access({"user_id": user.id})
        refresh = JWTToken.get_refresh()

        JWT.objects.create(user_id=user.id, access=access, refresh=refresh)

        return Response({"access": access, "refresh": refresh})


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        CustomUser.objects._create_user(**serializer.validated_data)

        return Response({"success": "User created"}, status=201)


class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt=JWT.objects.get(
                refresh=serializer.validated_data['refresh'])
        except JWT.DoesNotExist:
            return Response({"error": "refresh token not found"}, status=400)

        if not Authentication.verify_token(serializer.validated_data['refresh']):
            return Response({"error": "Token is invalid or has expired"})

        access = JWTToken.get_access({"user_id": active_jwt.user.id})
        refresh = JWTToken.get_refresh()

        active_jwt.access=access
        active_jwt.refresh=refresh
        active_jwt.save()

        return Response({"access": access, "refresh": refresh})


class FileUploadView(ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer


class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedCustom, )

    def get_queryset(self):

        if self.request.method.lower() != 'get':
            return self.queryset
        
        data = self.request.query_params.dict()
        data.pop('page', None)
        keyword = data.pop('keyword', None)

        if keyword:
            search_fields = ('user__username', 'user__name', 'first_name', 'last_name')
            query = self.get_query(keyword, search_fields)

            try:
                return self.queryset.filter(query).filter(**data).exclude(Q(user__id=self.request.user.id) | Q(user__is_superuser=True)).distinct()
            except Exception as e:
                raise Exception(e)
        
        return self.queryset.filter(**data).exclude(Q(user__id=self.request.user.id) | Q(user__is_superuser=True)).distinct()

    @staticmethod
    def get_query(query_string, search_fields):
        query = None  
        terms = UserProfileView.normalize_query(query_string)
        
        for term in terms:
            or_query = None 
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query
    
    @staticmethod
    def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

    def update(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except:
            pass

        instance = self.get_object()

        file_upload = request.data.pop('file_upload', None)
        serializer = self.serializer_class(data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if file_upload:
            try:
                file_ = FileUpload.objects.create(**file_upload)
                profile = self.get_object()
                profile.profile_picture = file_
                profile.save()
                profile = self.get_object()
                return Response(self.serializer_class(profile).data, status=200)
            except Exception:
                return Response({"error": "failed to upload profile picture"}, status=400)
        
        return Response(serializer.data, status=200)


class MeView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedCustom, )

    def get(self, request):
        data = {}

        try:
            data = self.serializer_class(request.user.user_profile).data
        except Exception:
            data = {
                'user': {
                    'id': request.user.id
                }
            }
            
        return Response(data, status=200)


class LogoutView(APIView):
    permission_classes = (IsAuthenticatedCustom,)

    def get(self, request):
        user_id = request.user.id

        JWT.objects.filter(user_id=user_id).delete()

        return Response("logged out successfully", status=200)