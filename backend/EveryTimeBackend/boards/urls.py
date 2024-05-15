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

    path("get/posts/", # 특정 게시판 내 게시글 요청 (pagination/keyword 서치 포함)
        views.boards_get_posts_view.as_view(),
        name='boards.get_posts'),

    path("admin/", # 특정 게시판 내 게시글 요청 (pagination/keyword 서치 포함)
         views.boards_admin_view.as_view(),
         name='boards.admin'),
]