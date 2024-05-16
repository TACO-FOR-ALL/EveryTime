from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display=[
        'get_board_name',
        'title',
        'get_author_username',
        'get_author_nickname',
        'get_like_num',
        'views',
        'created_at',
        'last_modified',
        'pending',
        'is_deleted'
    ]
    search_fields=[
        'board__name',
        'author__username',
        'author__nickname',
        'title'
    ]

    def get_author_username(self, obj):
        return obj.author.username
    get_author_username.short_description = 'Author Username'

    def get_author_nickname(self, obj):
        return obj.author.nickname
    get_author_nickname.short_description = 'Author Nickname'

    def get_board_name(self, obj):
        return obj.board.name
    get_board_name.short_description = 'Board Name'

    def get_like_num(self, obj):
        return obj.like_users.count()

admin.site.register(Post, PostAdmin)