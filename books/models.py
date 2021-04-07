from django.db import models
from user.models import CustomUser, UserProfile, FileUpload


class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    uploaded_by = models.OneToOneField(CustomUser, related_name='book_uploader', on_delete=models.CASCADE)
    authers = models.ForeignKey(UserProfile, related_name='book_authers', on_delete=models.CASCADE)
    category = models.OneToOneField(Category, related_name='book_category', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pages = models.IntegerField()
    description = models.TextField()
    book = models.OneToOneField(FileUpload, related_name='book_file', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('created_at',)
