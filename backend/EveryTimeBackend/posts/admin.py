from django.contrib import admin
from .models import *

class PostMediaAdmin(admin.ModelAdmin):
    list_display=[
        'get_post_title',
        'url'
    ]
    search_fields=[
        'post__title',
        'post__author__username'
    ]

    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = 'Post title'

class PostAdmin(admin.ModelAdmin):
    list_display=[
        'get_board_name',
        'title',
        'get_author_name',
        'created_at',
        'last_modified'
    ]
    search_fields=[
        'board__name',
        'author__username',
        'title'
    ]

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.username
        else: # 게시글 작성자 계정이 삭제된 경우
            return 'NULL'
    get_author_name.short_description = 'Author Username'

    def get_board_name(self, obj):
        return obj.board.name
    get_board_name.short_description = 'Board Name'

admin.site.register(PostMedia, PostMediaAdmin)
admin.site.register(Post, PostAdmin)