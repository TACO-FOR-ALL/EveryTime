from django.contrib import admin

from .models import PostMedia

class PostMediaAdmin(admin.ModelAdmin):
    list_display=[
        'get_post_title',
        'object_key'
    ]
    search_fields=[
        'post__title',
        'post__author__username'
    ]

    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = 'Post title'

admin.site.register(PostMedia, PostMediaAdmin)