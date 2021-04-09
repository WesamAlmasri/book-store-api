from rest_framework import serializers
from .models import Category, Auther, Book, BookImage, BookComment
from user.serializers import CustomUserSerializer, UserProfileSerializer, FileUploadSerializer

class CategorySerializer(serializers.Serializer):
    name = serializers.CharField()

class AutherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Auther
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    uploaded_by = CustomUserSerializer(read_only=True)
    uploaded_by_id = serializers.IntegerField(write_only=True)
    auther = AutherSerializer(read_only=True)
    auther_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    file = FileUploadSerializer(read_only=True)
    file_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class BookImageSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    image = FileUploadSerializer(read_only=True)
    image_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookImage
        fields = '__all__'

class BookCommentSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookComment
        dields = '__all__'