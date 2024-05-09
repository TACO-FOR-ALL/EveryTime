from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import *
from .utils import CheckBoardPermission

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
        Developer: Macchiato
        API: /boards/set/main_board
        기능: 유저의 메인 게시판에 대한 조작
    """
    def post(self, request: Request):
        user = self.get_user()
        try:
            user_board_profile = UserBoardProfile.objects.get(user=user)
            new_main_board_info = {}
            new_main_board_id = 0
            new_main_is_delete = False

            try:
                new_main_board_info = request.data.get('main_board')
                if new_main_board_info is None:
                    raise KeyError
                new_main_board_id = new_main_board_info['board_id']
                new_main_is_delete = new_main_board_info['is_delete']
            except KeyError:
                return Response(
                data=ResponseContent.fail('잘못된 요청 파라미터!'),
                status=status.HTTP_400_BAD_REQUEST
            )

            if new_main_is_delete: # 삭제 조작
                try:
                    with transaction.atomic():
                        user_board_profile.main_board = None
                        user_board_profile.save()
                    return Response(
                        data=ResponseContent.success()
                    )
                except Exception as e:
                    # TODO: LOGGING
                    raise e

            # 설정/변경 조작
            try:
                new_main_board = BaseBoard.objects.get(id=new_main_board_id)
                if not CheckBoardPermission(user, new_main_board): # 열람 권한 없음
                    return Response(
                        data=ResponseContent.fail("해당 게시판에 대한 권한이 없습니다!"),
                        status=status.HTTP_400_BAD_REQUEST
                    )
                with transaction.atomic():
                    user_board_profile.main_board = new_main_board
                    user_board_profile.save()
                
                return Response(
                    data=ResponseContent.success()
                )
            except Exception as e:
                # TODO: LOGGING
                raise e

        except:
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class boards_set_bookmark_boards_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /boards/set/bookmark_boards
        기능: 유저의 즐겨찾기 게시판에 대한 조작
    """
    def post(self, request):
        user = self.get_user()
        try:
            user_board_profile = UserBoardProfile.objects.get(user=user)
            new_fav_board_info = {}
            new_fav_board_id = 0
            new_fav_is_delete = False

            try:
                new_fav_board_info = request.data.get('favorite_board')
                if new_fav_board_info is None:
                    raise KeyError
                new_fav_board_id = new_fav_board_info['board_id']
                new_fav_is_delete = new_fav_board_info['is_delete']
            except KeyError:
                return Response(
                data=ResponseContent.fail('잘못된 요청 파라미터!'),
                status=status.HTTP_400_BAD_REQUEST
            )

            if new_fav_is_delete: # 삭제 조작
                try:
                    with transaction.atomic():
                        board_to_delete = BaseBoard.objects.get(id=new_fav_board_id)
                        user_board_profile.favorite_boards.remove(board_to_delete)
                        user_board_profile.save()

                    return Response(
                        data=ResponseContent.success()
                    )
                except Exception as e:
                    # TODO: LOGGING
                    raise e

            # 설정 조작
            try:
                new_fav_board = BaseBoard.objects.get(id=new_fav_board_id)
                if not CheckBoardPermission(user, new_fav_board): # 열람 권한 없음
                    return Response(
                        data=ResponseContent.fail("해당 게시판에 대한 권한이 없습니다!"),
                        status=status.HTTP_400_BAD_REQUEST
                    )
                with transaction.atomic():
                    user_board_profile.favorite_boards.add(new_fav_board)
                    user_board_profile.save()
                
                return Response(
                    data=ResponseContent.success()
                )
            except Exception as e:
                # TODO: LOGGING
                raise e

        except:
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )