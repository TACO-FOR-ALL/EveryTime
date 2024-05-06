from django.contrib import admin
from .models import *

class BoardAdmin(admin.ModelAdmin):
    list_display=[
        'name',
        'created_at'
    ]
    search_fields=[
        'name'
    ]

    # def get_organization_name(self, obj):
    #     return obj.organization.name
    # get_organization_name.short_description = 'Organization Name'

class PostAdmin(admin.ModelAdmin):
    list_display=[
        'get_board_name',
        'title',
        'author',
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
            return 'SYSTEM'
    get_author_name.short_description = 'Author Username'

    def get_board_name(self, obj):
        return obj.organization.name
    get_board_name.short_description = 'Board Name'

#admin.site.register(Board, BoardAdmin)
admin.site.register(Post, PostAdmin)