from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from posts.models import Post
from boards.utils import CheckBoardPermission
from .utils import (
    get_usercode_list_for_comments_of_post,
    get_comments_of_post_by_num,
    get_num_of_reply_comment
)

from EveryTimeBackend.view_template import LoginNeededView
from EveryTimeBackend.utils import ResponseContent

class comments_get_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /comments/get/comments/?postid=<id>&timestamp=<timestamp>&num=<num>
        기능: 특정 게시글에 해당되는 댓글 리턴
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            post_id = request.query_params.get('posttid', None)
            num = request.query_params.get('num', None)
            ts = request.query_params.get('timestamp', None)
            
            if post_id is None:
                return Response(
                    data=ResponseContent.fail('postid 미제공!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            if num is None:
                return Response(
                    data=ResponseContent.fail('num 미제공!'),
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
                userlist = get_usercode_list_for_comments_of_post(obj_post) # 댓글을 단 유저 리스트
                result = []
                if ts: # pagination
                    comments = get_comments_of_post_by_num(post=obj_post,
                                                           ts=ts,
                                                           num=num)
                else: # 첫 요청
                    comments = get_comments_of_post_by_num(post=obj_post,
                                                           num=num)
                    
                for comment in comments:
                    cur_dict = {
                        'comment_id': comment.id,
                        'author_num': userlist[comment.author.username], # 리스트에서 username으로 넘버 획득
                        'content': comment.content,
                        'timestamp': comment.created_at.timestamp(),
                        'created_at': comment.created_at_readable,
                        'reply_num': get_num_of_reply_comment(comment), # 해당 댓글에 대한 답글 갯수 획득
                        'is_deleted': comment.is_deleted
                    }
                    result.append(cur_dict)

                return Response(
                    data=ResponseContent.success(
                        data=result,
                        data_field_name='comments'
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