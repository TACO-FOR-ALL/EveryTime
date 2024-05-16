from django.urls import path

from . import views

"""
    URL prefix: /comments/
"""
urlpatterns = [
    path("get/comments/", # 지정 게시글의 댓글 획득
         views.comments_get_view.as_view(), 
         name='comments.get'),

    path("upload/comment", # 지정 게시글의 댓글 획득
         views.comments_upload_comment_view.as_view(), 
         name='comments.upload.comment'),

    path("upload/reply", # 지정 게시글의 댓글 획득
         views.comments_upload_reply_view.as_view(), 
         name='comments.upload.reply'),
]