from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from EveryTimeBackend.view_template import LoginNeededView

class boards_main_board_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /boards/main_board
        기능: 요청을 보낸 유저가 등록한 메인 게시판 관련 정보 리턴
    """

    def get(self, request):
        user = self.get_user()
        raise NotImplementedError
        # TODO

class boards_bookmark_boards_view(LoginNeededView):
    """
        Developer: 
        API: /boards/bookmark_boards
        기능: 요청을 보낸 유저가 즐겨찾기한 게시판 관련 정보 리턴
    """

    def get(self, request):
        raise NotImplementedError
        # TODO