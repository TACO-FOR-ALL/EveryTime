from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import *
from EveryTimeBackend.utils import ResponseContent


class posts_main_board_view(APIView):
    """
        Developer: 
        API: /posts/main_board
        기능: 요청을 보낸 유저가 등록한 메인 게시판 관련 정보 리턴
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raise NotImplementedError
        # TODO

class posts_bookmark_boards_view(APIView):
    """
        Developer: 
        API: /posts/bookmark_boards
        기능: 요청을 보낸 유저가 즐겨찾기한 게시판 관련 정보 리턴
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raise NotImplementedError
        # TODO

class posts_get_realtime_best_view(APIView):
    """
        Developer: 
        API: /posts/get_realtime_best
        기능: 실시간 베스트 게시글 목록 리턴
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raise NotImplementedError
        # TODO

class posts_get_view(APIView):
    """
        Developer: 
        API: /posts/get/?postid=<id>
        기능: 
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        post_id = request.GET.get('postid', None)
        
        if post_id is None:
            return Response(data=ResponseContent.fail(error_msg='postid 미제공!'),
                            status=status.HTTP_400_BAD_REQUEST)
        
        raise NotImplementedError
        # TODO