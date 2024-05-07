from django.urls import path

from . import views

"""
    URL prefix: /users/
"""
urlpatterns = [
        
    path("get_realtime_best", # 실시간 베스트 게시글 목록
         views.posts_get_realtime_best_view.as_view(),
         name='posts.get_realtime_best'),
    
    path("get/", # 게시글 내용
         views.posts_get_view.as_view(),
         name='posts.get'),
]