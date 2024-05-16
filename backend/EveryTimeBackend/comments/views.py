from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from posts.models import Post
from boards.utils import CheckBoardPermission, CheckIfBoardAdmin
from .utils import (
    get_usercode_list_for_comments_of_post,
    get_comments_of_post_by_num,
    get_reply_comment,
    get_num_of_reply_comment
)
from .models import Comment, UserCommentProfile

from EveryTimeBackend.view_template import LoginNeededView
from EveryTimeBackend.utils import ResponseContent

from typing import List

class comments_get_comments_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /comments/get/comments/?postid=<id>&timestamp=<timestamp>&num=<num>
        기능: 지정 게시글에 해당되는 댓글 리턴
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            post_id = request.query_params.get('postid', None)
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
                obj_post = Post.objects.get(id=post_id,
                                            pending=False,
                                            is_deleted=False)
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
                        'content': '' if comment.is_deleted else comment.content,
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
        
class comments_get_reply_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /comments/get/repy/?commentid=<id>&timestamp=<timestamp>&num=<num>
        기능: 지정 댓글에 해당되는 답글 리턴
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            comment_id = request.query_params.get('commentid', None)
            num = request.query_params.get('num', None)
            ts = request.query_params.get('timestamp', None)
            
            if comment_id is None:
                return Response(
                    data=ResponseContent.fail('commentid 미제공!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            if num is None:
                return Response(
                    data=ResponseContent.fail('num 미제공!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            obj_comment = None
            try: # 해당 id의 comment 검색
                obj_comment = Comment.objects.get(id=comment_id)
            except:
                return Response(
                    data=ResponseContent.fail('잘못된 commentid!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 해당 게시판에 대한 권한 없음
            if not CheckBoardPermission(user=user, board=obj_comment.post.board):
                return Response(
                    data=ResponseContent.fail('해당 게시판에 대한 권한이 없습니다!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try: # 리턴
                userlist = get_usercode_list_for_comments_of_post(obj_comment.post) # 댓글을 단 유저 리스트
                result = []
                if ts: # pagination
                    comments: List[Comment] = get_reply_comment(post=obj_comment,
                                                 ts=ts,
                                                 num=num)
                else: # 첫 요청
                    comments: List[Comment] = get_reply_comment(post=obj_comment,
                                                 num=num)
                    
                for comment in comments:
                    cur_dict = {
                        'comment_id': comment.id,
                        'author_num': userlist[comment.author.username], # 리스트에서 username으로 넘버 획득
                        'content': '' if comment.is_deleted else comment.content,
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
        
class comments_upload_comment_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /comments/upload/comment
        기능: 지정 게시글에 댓글 등록
    """
    def post(self, request: Request):
        user=self.get_user(request)
        try:
            post_id_to_use = request.data.get('post_id', None)
            content_to_use = request.data.get('content', None)

            if not (post_id_to_use and content_to_use):
                return Response(
                    data=ResponseContent.fail('필수 파라미터 부재!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            obj_post=None
            try:
                obj_post = Post.objects.get(id=post_id_to_use,
                                            pending=False,
                                            is_deleted=False)
            except:
                return Response(
                    data=ResponseContent.fail('잘못된 post_id!'),
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(content_to_use) > 1024: # WARNING=BAD LOGIC
                return Response(
                    data=ResponseContent.fail('댓글 내용이 너무 깁니다!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not CheckBoardPermission(user, obj_post.board):
                return Response(
                    data=ResponseContent.fail('해당 게시판에 대한 권한이 없습니다!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                with transaction.atomic():
                    # 새로운 댓글 등록
                    new_comment=Comment(
                        author=user,
                        post=obj_post,
                        content=content_to_use
                    )
                    new_comment.save()

                    # 댓글 프로필에 추가
                    user_comment_profile=UserCommentProfile.objects.get(user=user)
                    user_comment_profile.comments.add(new_comment)
                    user_comment_profile.save()

                    return Response(
                        data=ResponseContent.success()
                    )
            except Exception as e:
                # TODO: LOGGING
                raise e

        except:
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class comments_upload_reply_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /comments/upload/reply
        기능: 지정 댓글에 답글 등록
    """
    def post(self, request: Request):
        user=self.get_user(request)
        try:
            comment_id_to_use = request.data.get('comment_id', None)
            content_to_use = request.data.get('content', None)

            if not (comment_id_to_use and content_to_use):
                return Response(
                    data=ResponseContent.fail('필수 파라미터 부재!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            obj_post=None
            obj_comment=None
            try:
                obj_comment = Comment.objects.get(id=comment_id_to_use)
                obj_post = obj_comment.post
            except:
                return Response(
                    data=ResponseContent.fail('잘못된 comment_id!'),
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(content_to_use) > 1024: # WARNING=BAD LOGIC
                return Response(
                    data=ResponseContent.fail('댓글 내용이 너무 깁니다!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not CheckBoardPermission(user, obj_post.board):
                return Response(
                    data=ResponseContent.fail('해당 게시판에 대한 권한이 없습니다!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                with transaction.atomic():
                    # 새로운 답글 등록
                    new_comment=Comment(
                        author=user,
                        post=obj_post,
                        content=content_to_use,
                        replying_to=obj_comment.id # 답글 id
                    )
                    new_comment.save()

                    # 댓글 프로필에 추가
                    user_comment_profile=UserCommentProfile.objects.get(user=user)
                    user_comment_profile.comments.add(new_comment)
                    user_comment_profile.save()

                    return Response(
                        data=ResponseContent.success()
                    )
            except Exception as e:
                # TODO: LOGGING
                raise e

        except:
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class comments_like(LoginNeededView):
    """
        Developer: Macchiato
        API: /comments/like/?commentid=<comment_id>&like=<like>`
        기능: 지정 댓글 좋아요 설정/해제
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            comment_id_to_use = request.query_params.get('commentid', None)
            like_status = request.query_params.get('like', None)

            if not (comment_id_to_use and like_status):
                return Response(
                    data=ResponseContent.fail('필수 파라미터 부재!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            like_status = int(like_status)
            if like_status != 1 and like_status != 0:
                return Response(
                    data=ResponseContent.fail(f'잘못된 like: {str(like_status)}'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            obj_comment=None
            try:
                obj_comment = Comment.objects.get(id=comment_id_to_use)
            except Exception as e:
                return Response(
                    data=ResponseContent.fail('잘못된 commentid!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                with transaction.atomic():
                    if like_status: # 좋아요 설정
                        obj_comment.like_users.add(user)
                    else: # 해제
                        obj_comment.like_users.delete(user)
                    obj_comment.save()
            except Exception as e:
                # TODO: LOGGING
                raise e
            
        except:
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class comments_delete(LoginNeededView):
    """
        Developer: Macchiato
        API: /comments/delete/?commentid=<comment_id>
        기능: 지정 댓글 삭제, 본인 또는 관리자만 요청 가능
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            comment_id_to_use = request.query_params.get('commentid', None)

            if comment_id_to_use is None:
                return Response(
                data=ResponseContent.fail('필수 파라미터 부재: commentid!'),
                status=status.HTTP_400_BAD_REQUEST
            )

            obj_comment=None
            try:
                obj_comment=Comment.objects.get(id=comment_id_to_use)
            except:
                return Response(
                data=ResponseContent.fail(f'잘못된 commentid={comment_id_to_use}'),
                status=status.HTTP_400_BAD_REQUEST
            )
            
            try:
                if user == obj_comment.author or CheckIfBoardAdmin(user=user, board=obj_comment.post.board):
                    # 본인 댓글 또는 해당 게시판 관리자인 경우에만 삭제 가능
                    with transaction.atomic():
                        obj_comment.is_deleted=True
                        obj_comment.save()
                        return Response(
                            data=ResponseContent.success()
                        )
                else: # 권한 없음
                    return Response(
                        data=ResponseContent.fail(f'해당 댓글에 대한 권한이 없습니다!'),
                        status=status.HTTP_400_BAD_REQUEST
                    )
                        
            except Exception as e:
                # TODO: LOGGING
                raise e

        except:
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )