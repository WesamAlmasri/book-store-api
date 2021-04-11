from django.db import models
from user.models import CustomUser, UserProfile, FileUpload


class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Auther(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user_auther', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    auther = models.ForeignKey(Auther, related_name='auther_books', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category_books', on_delete=models.CASCADE)
    file = models.OneToOneField(FileUpload, related_name='file_book', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pages = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('created_at',)

class BookImage(models.Model):
    book = models.ForeignKey(Book, related_name='book_images', on_delete=models.CASCADE)
    image = models.ForeignKey(FileUpload, related_name='image_book', on_delete=models.CASCADE)
    is_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.auther.name} - {self.book.title} - {self.image}"

class BookComment(models.Model):
    book = models.ForeignKey(Book, related_name='book_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='user_comments', on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.IntegerField(default=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)