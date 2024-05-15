from django.contrib import admin

from .models import PostMedia

class PostMediaAdmin(admin.ModelAdmin):
    list_display=[
        'get_post_title',
        'get_author_username',
        'get_author_nickname',
        'object_key'
    ]
    search_fields=[
        'post__title',
        'post__author__username',
        'post__author__nickname'
    ]

    def get_author_username(self, obj):
        return obj.post.author.username
    get_author_username.short_description = 'Author Username'

    def get_author_nickname(self, obj):
        return obj.post.author.nickname
    get_author_nickname.short_description = 'Author Nickname'

    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = 'Post title'

admin.site.register(PostMedia, PostMediaAdmin)