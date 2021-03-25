from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Username field is required')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_super_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FILED = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ('created_at',)

class FileUpload(models.Model):
    file_upload = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_upload}"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user_profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = models.ForeignKey(FileUpload, related_name='user_image', on_delete=models.SET_NULL, null=True)
    phone = models.PositiveIntegerField()
    country_code = models.CharField(default='+962', max_length=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ("created_at",)
    

class JWT(models.Model):
    user = models.OneToOneField(CustomUser, related_name='login_user', on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)