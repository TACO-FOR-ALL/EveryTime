from django.urls import path

from . import views

"""
    URL prefix: /comments/
"""
urlpatterns = [
    path("get/comments/", # 지정 게시글의 댓글 획득
         views.comments_get_comments_view.as_view(), 
         name='comments.get.comments'),

    path("get/reply/", # 지정 게시글의 댓글 획득
         views.comments_get_reply_view.as_view(), 
         name='comments.get.reply'),

    path("upload/comment", # 게시글 댓글 등록
         views.comments_upload_comment_view.as_view(), 
         name='comments.upload.comment'),

    path("upload/reply", # 댓글 답글 등록
         views.comments_upload_reply_view.as_view(), 
         name='comments.upload.reply'),

     path("like/", # 댓글 좋아요/좋아요 해제
         views.comments_like.as_view(), 
         name='comments.like'),

     path("delete/", # 댓글 삭제
         views.comments_delete.as_view(), 
         name='comments.delete'),
]