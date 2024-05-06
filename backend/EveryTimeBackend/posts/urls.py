from django.urls import path

from . import views

"""
    URL prefix: /users/
"""
urlpatterns = [
    path("main_board", # 메인 게시판 정보
         views.posts_main_board_view.as_view(), 
         name='posts.main_board'), 
    
    path("bookmark_boards", # 즐겨찾기 게시판 목록
         views.posts_bookmark_boards_view.as_view(),
         name='posts.bookmark_boards'),
        
    path("get_realtime_best", # 실시간 베스트 게시글 목록
         views.posts_get_realtime_best_view.as_view(),
         name='posts.get_realtime_best'),
    
    path("get/", # 게시글 내용
         views.posts_get_view.as_view(),
         name='posts.get'),
]