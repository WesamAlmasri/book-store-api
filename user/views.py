from django.shortcuts import render
from .models import JWT, CustomUser
from .utils import JWTToken
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer, RefreshSerializer
from django.contrib.auth import authenticate
from .authentication import Authentication


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
