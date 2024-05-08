from django.urls import path

from . import views

"""
    URL prefix: /boards/
"""
urlpatterns = [
    path("get/main_board", # 메인 게시판 정보
         views.boards_get_main_board_view.as_view(), 
         name='boards.main_board'), 
    
    path("get/bookmark_boards", # 즐겨찾기 게시판 목록
         views.boards_get_bookmark_boards_view.as_view(),
         name='boards.bookmark_boards'),

    path("set/main_board", # 메인 게시판 설정 조작
         views.boards_set_main_board_view.as_view(), 
         name='boards.main_board'), 
    
    path("set/bookmark_boards", # 즐겨찾기 게시판 설정 조작
         views.boards_set_bookmark_boards_view.as_view(),
         name='boards.bookmark_boards'),
]