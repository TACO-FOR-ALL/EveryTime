from django.urls import path

from . import views

"""
    URL prefix: /users/
"""
urlpatterns = [
        
    path("realtime_best", # 실시간 베스트 게시글 목록
         views.posts_realtime_best_view.as_view(),
         name='posts.get_realtime_best'),
    
    path("get/", # 게시글 내용
         views.posts_get_view.as_view(),
         name='posts.get'),

    path("upload", # 게시글 업로드
         views.posts_upload_view.as_view(),
         name='posts.upload'),

    path("upload/fail", # 게시글 업로드 실패 고지
         views.posts_upload_fail_view.as_view(),
         name='posts.upload.fail'),

     path("like/", # 게시글 좋아요 설정/해제
         views.posts_like_view.as_view(),
         name='posts.like'),

     path("delete/", # 게시글 삭제
         views.posts_delete_view.as_view(),
         name='posts.delete'),

]