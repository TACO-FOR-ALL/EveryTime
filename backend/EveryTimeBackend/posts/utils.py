from django.utils.dateparse import parse_datetime

from boards.models import BaseBoard
from .models import Post

from datetime import datetime
from typing import List


def get_board_post_by_num(board: BaseBoard,
                          ts: str,
                          num: int) -> List[Post]:
    """
        게시글 획득:
        1. 지정한 게시판 'board'의
        2. timestamp가 'ts'보다 오래된 (ts가 None일 시 제일 최신의 것들을 리턴)
        3. 'num'개 획득

        주의: 
        1. 먼저 요청한 유저의 'board'에 대한 권한을 체크한 후 해당 함수 call
        2. 'num'보다 적거나 0개를 리턴할 수도 있음
        3. Post instance의 리스트를 리턴
    """
    if ts: # pagination
        last_seen_datetime = datetime.fromtimestamp(float(ts))
        posts = Post.objects.filter(
            board=board,
            created_at__lt=last_seen_datetime
            ).order_by('-created_at')[:num]
    else: # 최신 게시글
        posts = Post.objects.filter(
            board=board
        ).order_by('-created_at')[:num]

    return posts


def check_post_if_match_keyword(post: Post,
                                keyword: str) -> bool:
    """
        목표 게시글 'post'의:
        1. 제목
        2. 내용
        에 'keyword'가 포함되어 있는지 체크하고 결과를 리턴
    """
    return (keyword in post.title) or (keyword in post.content)