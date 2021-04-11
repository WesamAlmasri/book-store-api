from django.contrib import admin
from .models import Category, Auther, Book, BookImage, BookComment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(Category, CategoryAdmin)


class AutherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'created_at')
    list_display_links = ('id', 'user', 'name')
    search_fields = ('user__username', 'name')
    list_per_page = 25

admin.site.register(Auther, AutherAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'auther', 'category', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'auther__name')
    list_per_page = 25

admin.site.register(Book, BookAdmin)

class BookImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'is_cover', 'created_at')
    list_display_links = ('id', 'book')
    search_fields = ('book__title',)
    list_per_page = 25

admin.site.register(BookImage, BookImageAdmin)

class BookCommentImageAd(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'rate', 'created_at')
    list_display_links = ('id', 'book')
    search_fields = ('book__title',)
    list_per_page = 25

admin.site.register(BookComment, BookCommentImageAd)