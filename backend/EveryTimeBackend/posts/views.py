from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import *
from EveryTimeBackend.utils import ResponseContent
from EveryTimeBackend.view_template import LoginNeededView

class posts_realtime_best_view(LoginNeededView):
    """
        Developer: 
        API: /posts/realtime_best
        기능: 실시간 베스트 게시글 목록 리턴
    """
    def get(self, request):
        raise NotImplementedError
        # TODO

class posts_get_view(LoginNeededView):
    """
        Developer: 
        API: /posts/get/?postid=<id>
        기능: 
    """
    def get(self, request: Request):
        post_id = request.query_params.get('postid', None)
        
        if post_id is None:
            return Response(data=ResponseContent.fail(error_msg='postid 미제공!'),
                            status=status.HTTP_400_BAD_REQUEST)
        
        raise NotImplementedError
        # TODO