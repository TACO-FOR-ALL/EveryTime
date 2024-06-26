from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from medias.utils import get_media_upload_dict
from boards.models import BaseBoard
from boards.utils import CheckBoardPermission, CheckIfBoardAdmin
from .models import *
from .utils import get_post_media_download_urls, check_post_if_with_media

from EveryTimeBackend.utils import ResponseContent
from EveryTimeBackend.view_template import LoginNeededView

from loguru import logger

class posts_realtime_best_view(LoginNeededView):
    """
        Developer: 
        API: /posts/realtime_best
        기능: 실시간 베스트 게시글 목록 리턴
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            posts=Post.objects.filter(
                pending=False,
                is_deleted=False
            ).order_by('views')\
             .order_by('-created_at')[:5] # 먼저 조회수 순으로 정렬, 그리고 최신순으로 정렬
            
            result = []
            for post in posts:
                cur_dict = {
                        "is_media": check_post_if_with_media,
                        "title": post.title,
                        "post_id": post.id,
                        "board_name": post.board.name,
                        "board_id": post.board.id,
                        "nickname": "",
                        "like_num": post.like_users.count(),
                        "views": post.views,
                        "created_at": post.created_at_readable
                }
                if not post.anonymous: # 비익명 게시글
                    cur_dict['nickname']=post.author.nickname
                if user == post.author: # 본인 게시글
                    cur_dict['nickname']='나'
                
                result.append(cur_dict)
            
            return Response(
                data=ResponseContent.success(
                    data=result,
                    data_field_name='posts'
                )
            )
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("requesting_user: " + user.username)
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
                result = {
                    'media_urls': get_post_media_download_urls(obj_post),
                    'title': obj_post.title,
                    'board_name': obj_post.board.name,
                    'board_id':obj_post.board.id,
                    'created_at':obj_post.created_at_readable,
                    'nickname': '',
                    'like_num': obj_post.like_users.count(),
                    'views': obj_post.views
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
                logger.debug("Error at post get")
                logger.debug("Post id: " + str(obj_post.id))
                raise e
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("requesting_user: " + user.username)
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class posts_upload_view(LoginNeededView):
    def post(self, request: Request):
        user=self.get_user(request)
        try:
            board_id_to_use = request.data.get('board_id', None)
            title_to_use = request.data.get('title', None)
            anonymous_to_use = request.data.get('anonymous', None)
            content_to_use = request.data.get('content', None)
            file_num_to_use = request.data.get('file_num', None)

            if not (board_id_to_use and title_to_use and anonymous_to_use and content_to_use and file_num_to_use):
                return Response(
                    data=ResponseContent.fail('필수 파라미터 부재'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 파라미터 전환1
            try:
                anonymous_to_use = bool(anonymous_to_use)
            except:
                return Response(
                    data=ResponseContent.fail('잘못된 형식의 anonymous, boolean 형식 필요'),
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # 파라미터 전환2    
            try:
                file_num_to_use = int(file_num_to_use)
                if file_num_to_use < 0 or file_num_to_use > 4: # 1~4
                    raise Exception()
            except:
                return Response(
                    data=ResponseContent.fail('잘못된 형식의 anonymous, 1~4 사이의 int 형식 필요'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 목표 게시판
            obj_board=None
            try:
                obj_board=BaseBoard.objects.get(id=board_id_to_use)
            except Exception as e:
                return Response(
                    data=ResponseContent.fail('잘못된 board_id'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if CheckBoardPermission(user, obj_board):
                return Response(
                    data=ResponseContent.fail('해당 게시판에 대한 권한이 없습니다!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                with transaction.atomic(): # 게시글 object 생성
                    new_post = Post(
                        title=title_to_use,
                        content=content_to_use,
                        author=user,
                        board=obj_board,
                        anonymous=anonymous_to_use
                    )

                    if file_num_to_use == 0: # 미디어 없음
                        new_post.pending=False # 대기 상태 해제, 바로 열람 가능
                    new_post.save() # 일단 저장

                    # 게시글 프로필에 추가
                    user_post_profile=UserPostProfile.objects.get(user=user)
                    user_post_profile.posts.add(new_post)
                    user_post_profile.save()

                    medias = [] # 업로드용 임시 url
                    if file_num_to_use >= 1: # 미디어 있음
                        # TODO: upload_url/callback_url/callback_payload 구성
                        obj_post_id = new_post.id
                        for index in range(file_num_to_use):
                            medias.append(get_media_upload_dict(
                                prefix='posts',
                                id=obj_post_id,
                                index=index,
                                obj=new_post
                            ))

                    result = {
                        "medias": medias,
                        "post_id": new_post.id
                    }

                    return Response(
                        data=ResponseContent.success(
                            data=result
                        )
                    )
            except Exception as e:
                logger.debug("Error at new post save")
                logger.debug("Board id: " + str(obj_board.id))
                raise e

        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("requesting_user: " + user.username)
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 

class posts_upload_fail_view(LoginNeededView):
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            post_id_to_use = request.query_params.get('postid', None)

            if post_id_to_use is None:
                return Response(
                    data=ResponseContent.fail('필수 파라미터 부재: postid'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            obj_post=None # 목표 게시글
            try:
                obj_post = Post.objects.get(id=post_id_to_use,
                                            pending=False,
                                            is_deleted=False)
            except:
                return Response(
                    data=ResponseContent.fail('잘못된 postid'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                with transaction.atomic(): # 대기 중 게시글 삭제
                    # TODO: 이미 업로드가 완료된 PostMedia를 OSS에서도 삭제할 것인지?
                    obj_post.delete()
                    # 관련 PostMedia Object 자동 삭제
                    # 게시글 프로필에서 자동 삭제

                    return Response(
                        data=ResponseContent.success()
                    )
            except Exception as e:
                logger.debug("Error at post delete")
                logger.debug("Post id: " + str(obj_post.id))
                raise e

        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("requesting_user: " + user.username)
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class posts_like_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /posts/like/?postid=<post_id>&like=<like>
        기능: 지정 게시글 좋아요 설정/해제
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            post_id_to_use = request.query_params.get('postid', None)
            like_status = request.query_params.get('like', None)

            if not (post_id_to_use and like_status):
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
            
            obj_post=None
            try:
                obj_post = Post.objects.get(id=post_id_to_use,
                                            pending=False,
                                            is_deleted=False)
            except Exception as e:
                return Response(
                    data=ResponseContent.fail('잘못된 postid!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                with transaction.atomic():
                    if like_status: # 좋아요 설정
                        obj_post.like_users.add(user)
                    else: # 해제
                        obj_post.like_users.delete(user)
                    obj_post.save()
            except Exception as e:
                logger.debug("Error at post like set save")
                logger.debug("Post id: " + str(obj_post.id))
                raise e
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("requesting_user: " + user.username)
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class posts_delete_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /posts/delete/?postid=<post_id>
        기능: 지정 게시글 삭제 (본인 또는 게시판 관리자)
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            post_id_to_use = request.query_params.get('posttid', None)

            if post_id_to_use is None:
                return Response(
                data=ResponseContent.fail('필수 파라미터 부재: postid!'),
                status=status.HTTP_400_BAD_REQUEST
            )

            obj_post=None
            try:
                obj_post=Post.objects.get(id=post_id_to_use,
                                          pending=False,
                                          is_deleted=False)
            except:
                return Response(
                data=ResponseContent.fail(f'잘못된 postid={post_id_to_use}'),
                status=status.HTTP_400_BAD_REQUEST
            )
            
            try:
                if user == obj_post.author or CheckIfBoardAdmin(user=user, board=obj_post.board):
                    # 본인 게시글 또는 해당 게시판 관리자인 경우에만 삭제 가능
                    with transaction.atomic():
                        obj_post.is_deleted=True
                        obj_post.save()
                        return Response(
                            data=ResponseContent.success()
                        )
                else: # 권한 없음
                    return Response(
                        data=ResponseContent.fail(f'해당 게시글에 대한 권한이 없습니다!'),
                        status=status.HTTP_400_BAD_REQUEST
                    )
                        
            except Exception as e:
                logger.debug("Error at post delete save")
                logger.debug("Post id: " + str(obj_post.id))
                raise e

        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("requesting_user: " + user.username)
            return Response(
                data=ResponseContent.fail('서버 에러!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )