from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from posts.utils import get_board_post_by_num, check_post_if_match_keyword, check_post_if_with_media
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
            user_board_profile=None
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
                new_main_board=None
                try:
                    new_main_board = BaseBoard.objects.get(id=new_main_board_id)
                except:
                    return Response(
                        data=ResponseContent.fail('잘못된 main_board_id!'),
                        status=status.HTTP_400_BAD_REQUEST
                    )
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
                new_fav_board=None
                try:
                    new_fav_board = BaseBoard.objects.get(id=new_fav_board_id)
                except:
                    return Response(
                        data=ResponseContent.fail('잘못된 fav_board_id!'),
                        status=status.HTTP_400_BAD_REQUEST
                    )
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
        
class boards_get_posts_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /boards/get/posts/?boardid=<id>&timestamp=<timestamp>&num=<num>&keyword=<keyword>
        기능: 지정 게시판 내 게시글 (Pagination/Search 가능) 획득
    """
    def get(self, request: Request):
        user = self.get_user()
        try:
            board_id = request.query_params.get('boardid', None)
            last_seen_timestamp = request.query_params.get('timestamp', None)
            num = request.query_params.get('num', None)
            keyword = request.query_params.get('keyword', None)

            if board_id is None or num is None: # 필수 파라미터 부재
                return Response(
                    data=ResponseContent.fail('필수 파라미터 부재!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            num = int(num)
            if num <= 0: # num은 0 이상이어야 함
                return Response(
                    data=ResponseContent.fail('무효한 파라미터: num'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 목표 게시판
            obj_board=None
            try: # 목표 게시판 query
                obj_board = BaseBoard.objects.get(id=board_id)
            except Exception as e:
                return Response(
                    data=ResponseContent.fail('잘못된 boardid'),
                    status=status.HTTP_400_BAD_REQUEST
                )

            try: # 게시판 권한 체크
                if not CheckBoardPermission(user, obj_board): # 해당 게시판 권한 없음
                    return Response(
                        data=ResponseContent.fail('해당 게시판에 대한 권한이 없습니다!'),
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                # TODO: LOGGING
                raise e
            
            post_result = []
            if keyword is None:
                try: # 비검색 획득
                    posts = get_board_post_by_num(board=obj_board,
                                                  ts=last_seen_timestamp,
                                                  num=num)
                    for post in posts:
                        post_result.append({
                            "is_media": check_post_if_with_media(post),
                            "title": post.title,
                            "post_id": post.id,
                            "board_name": post.board.name,
                            "board_id": post.board.id,
                            "timestamp": post.created_at.timestamp(),
                            "created_at": post.created_at_readable
                        })
                        
                    return Response(
                        data=ResponseContent.success(
                            data=post_result,
                            data_field_name='posts'
                        )
                    )
                except Exception as e:
                    # TODO: LOGGING
                    raise e
                
            # 검색 획득
            try:
                ts = last_seen_timestamp
                while len(post_result) < num: # num까지 채울 때까지 계속 진행
                    posts = get_board_post_by_num(board=obj_board,
                                                  ts=ts,
                                                  num=num)
                    for post in posts:
                        if check_post_if_match_keyword(post, keyword): # keyword 매치
                            post_result.append({
                            "is_media": check_post_if_with_media(post),
                            "title": post.title,
                            "post_id": post.id,
                            "board_name": post.board.name,
                            "board_id": post.board.id,
                            "timestamp": post.created_at.timestamp(),
                            "created_at": post.created_at_readable
                        })
                            
                    if len(post_result) >= num: # 위의 for에서 num을 초과해서 채웠을 경우 num만큼 짜르고 break
                        post_result = post_result[:num]
                        break
                    if len(posts) < num: # 더 이상 검색 가능한 post가 없음 [0, num)
                        break
                    
                    # 더 검색 진행 시
                    ts = posts[-1].created_at.timestamp() # 관련 ts를 현재 체크를 완료한 제일 오래된 post의 timestamp로 변경

                return Response(
                    data=ResponseContent.success(
                        data=post_result,
                        data_field_name='posts'
                    )
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