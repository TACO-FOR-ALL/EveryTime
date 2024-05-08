from django.urls import path

from . import views

"""
    URL prefix: /boards/
"""
urlpatterns = [
    path("main_board", # 메인 게시판 정보
         views.boards_main_board_view.as_view(), 
         name='boards.main_board'), 
    
    path("bookmark_boards", # 즐겨찾기 게시판 목록
         views.boards_bookmark_boards_view.as_view(),
         name='boards.bookmark_boards'),
]