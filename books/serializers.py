from rest_framework import serializers
from .models import Category, Book
from user.serializers import CustomUserSerializer, UserProfileSerializer, FileUploadSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class Book(serializers.ModelSerializer):
    uploaded_by = CustomUserSerializer(read_only=True)
    uploaded_by_id = serializers.IntegerField(write_only=True)
    auther = UserProfileSerializer(read_only=True)
    auther_id = serializers.IntegerField(write_only=True)
    category = CustomUserSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    book = FileUploadSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    cover_image = FileUploadSerializer(read_only=True)
    cover_image_id = serializers.IntegerField(write_only=True)
    

    class Meta:
        model = Book
        fields = '__all__'
