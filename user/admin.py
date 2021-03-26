from django.contrib import admin
from .models import CustomUser, UserProfile, JWT

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'created_at')
    list_display_links = ('id', 'username')
    list_editable = ('is_active',)
    search_fields = ('username', 'email')
    list_per_page = 25

admin.site.register(CustomUser, CustomUserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'created_at')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'user__email')
    list_per_page = 25

admin.site.register(UserProfile, UserProfileAdmin)


class JwtAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    list_display_links = ('id', 'user')
    search_fields = ('user_username', 'user__email')
    list_per_page = 25

admin.site.register(JWT, JwtAdmin)
