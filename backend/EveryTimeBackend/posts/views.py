from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from boards.utils import CheckBoardPermission
from .utils import get_post_media_download_urls
from .models import *
from EveryTimeBackend.utils import ResponseContent
from EveryTimeBackend.view_template import LoginNeededView

class posts_realtime_best_view(LoginNeededView):
    """
        Developer: 
        API: /posts/realtime_best
        기능: 실시간 베스트 게시글 목록 리턴
    """
    def get(self, request: Request):
        raise NotImplementedError
        # TODO

class posts_get_view(LoginNeededView):
    """
        Developer: 
        API: /posts/get/?postid=<id>
        기능: 게시글 내용 리턴
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            post_id = request.query_params.get('postid', None)
            
            if post_id is None:
                return Response(
                    data=ResponseContent.fail('postid 미제공!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            obj_post = None
            try: # 해당 id의 post 검색
                obj_post = Post.objects.get(id=post_id)
            except:
                return Response(
                    data=ResponseContent.fail('잘못된 postid!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 해당 게시판에 대한 권한 없음
            if not CheckBoardPermission(user=user, board=obj_post.board):
                return Response(
                    data=ResponseContent.fail('해당 게시판에 대한 권한이 없습니다!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try: # 리턴
                result = {
                    'media_urls': get_post_media_download_urls(),
                    'title': obj_post.title,
                    'board_name': obj_post.board.name,
                    'board_id':obj_post.board.id,
                    'created_at':obj_post.created_at_readable,
                    'nickname': ''
                }

                # 비익명 게시글일 시
                if not obj_post.anonymous:
                    result['nickname'] = obj_post.author.nickname
                # 본인 게시글일 시
                if obj_post.author == user:
                    result['nickname'] = '나'

                return Response(
                    data=ResponseContent.success(
                        data=result,
                        data_field_name='post'
                    )
                )
            except Exception as e:
                # TODO: LOGGING
                raise e
        except Exception as e:
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )