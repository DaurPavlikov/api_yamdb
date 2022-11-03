from django.contrib import admin

from .models import Review, Comment, Genre, Title, Category
from users.models import User

class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'role',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'author',
        'text',
        'pub_date'
    )
    search_fields = ('text', 'author')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name', )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name', )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
