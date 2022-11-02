from django.contrib import admin
from .models import Reviews, Comment


class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'author',
        'text',
        'pub_date'
    )
    search_fields = ('review',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Comment, CommentAdmin)
