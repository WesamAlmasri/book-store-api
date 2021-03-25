from rest_framework import serializers
from .models import CustomUser, UserProfile, FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    model = FileUpload
    fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exlude = ('password',)

class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile_picture = FileUploadSerializer(read_only=True)
    profile_picture_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'