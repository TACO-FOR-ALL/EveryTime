from rest_framework.response import Response
from rest_framework import status

from .models import *

from EveryTimeBackend.view_template import LoginNeededView
from EveryTimeBackend.utils import ResponseContent

class boards_get_main_board_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /boards/get/main_board
        기능: 요청을 보낸 유저가 등록한 메인 게시판 관련 정보 리턴
    """

    def get(self, request):
        user = self.get_user()
        try:
            user_board_profile = UserBoardProfile.objects.get(user=user)
            board_name = user_board_profile.main_board.name \
                if user_board_profile.main_board else ''
            board_id = user_board_profile.main_board.id \
                if user_board_profile.main_board else None

            return Response(
                data=ResponseContent.success(
                    data = {
                        board_name:board_name,
                        board_id:board_id
                    },
                    data_field_name='main_board'
                )
            )
                                    
        except:
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class boards_get_bookmark_boards_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /boards/get/bookmark_boards
        기능: 요청을 보낸 유저가 즐겨찾기한 게시판 관련 정보 리턴
    """

    def get(self, request):
        user = self.get_user()
        try:
            user_board_profile = UserBoardProfile.objects.get(user=user)
            favorite_boards = user_board_profile.favorite_boards.all()
            favorite_board_info_list = []
            for fboard in favorite_boards:
                fboard_info_dict = {
                    "board_name": fboard.name,
                    "board_name": fboard.id
                }
                favorite_board_info_list.append(fboard_info_dict)

            return Response(
                data=ResponseContent.success(
                    data=favorite_board_info_list,
                    data_field_name='boards'
                )
            )
        
        except:
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class boards_set_main_board_view(LoginNeededView):
    """
        Developer: 
        API: /boards/set/main_board
        기능: 유저의 메인 게시판에 대한 조작
    """
    def post(self, request):
        # TODO
        raise NotImplementedError

class boards_set_bookmark_boards_view(LoginNeededView):
    """
        Developer: 
        API: /boards/set/bookmark_boards
        기능: 유저의 즐겨찾기 게시판에 대한 조작
    """
    def post(self, request):
        # TODO
        raise NotImplementedError