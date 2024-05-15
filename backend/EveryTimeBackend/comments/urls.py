from django.urls import path

from . import views

"""
    URL prefix: /comments/
"""
urlpatterns = [
    path("get/comments/", # 지정 게시글의 댓글 획득
         views.comments_get_view.as_view(), 
         name='comments.get'),
]