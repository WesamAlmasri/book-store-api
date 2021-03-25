from django.shortcuts import render
from .models import JWT
from .utils import JWTToken
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer
from django.contrib.auth import authenticate


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        
        if not user:
            return Response({"error": "Invalid Username or Password"}, status=400)

        access = JWTToken.get_access({"user_id": user.id})
        refresh = JWTToken.get_refresh()
        
        JWT.objects.create(user_id=user.id, access=access, refresh=refresh)

        return Response({"access": access, "refresh": refresh})
