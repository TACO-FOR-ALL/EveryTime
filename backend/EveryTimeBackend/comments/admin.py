from django.contrib import admin

from .models import *

class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'get_post_title',
        'get_author_username',
        'get_author_nickname',
        'get_content_preview',
        'created_at'
    ]
    search_fields = [
        'post__title',
        'author__username',
        'author__nickname',
        'name'
    ]

    def get_content_preview(self, obj):
        """
            댓글 미리보기 리턴
        """
        return obj.content[:50]
    
    def get_author_username(self, obj):
        return obj.author.username
    
    def get_author_nickname(self, obj):
        return obj.author.nickname

    def get_post_title(self, obj):
        return obj.post.title
    
admin.site.register(Comment, CommentAdmin)