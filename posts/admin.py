from django.contrib import admin
from .models import Post, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'post_id',
        'user',
        'created',
    )

    fields = (
        'user',
        'congregation',
        'text_input',
        'likes',
        'bookmarks',
    )

    ordering = ('user',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post_id',
        'user',
        'created',
    )

    fields = (
        'original_post',
        'user',
        'congregation',
        'text_input',
        'likes',
        'bookmarks',
    )

    ordering = ('user',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)