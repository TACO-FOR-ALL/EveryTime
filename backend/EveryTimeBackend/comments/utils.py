from .models import Comment
from posts.models import Post

from typing import List, Dict

from datetime import datetime

def get_comments_of_post_by_num(post: Post,
                                ts: str,
                                num: int) -> List[Comment]:
    """
        댓글 획득:
        1. 지정한 게시판 'post'의
        2. timestamp가 'ts'와 같거나 오래된 (ts가 None일 시 제일 최신의 것들을 리턴)
        3. 'num'개 획득

        주의: 
        1. 먼저 요청한 유저의 'post'에 대한 권한을 체크한 후 해당 함수 call
        2. 'num'보다 적거나 0개를 리턴할 수도 있음
        3. Comment instance의 리스트를 리턴
        4. 게시글에 대한 직접적인 댓글만 리턴, 답글x
    """
    if ts: # pagination
        last_seen_datetime = datetime.fromtimestamp(float(ts))
        comments = Comment.objects.filter(
            post=post,
            replying_to=None, # 게시글에 대한 직접적인 답글
            created_at__lte=last_seen_datetime
            ).order_by('-created_at')[:num]
    else: # 최신 댓글
        comments = Comment.objects.filter(
            post=post,
            replying_to=None # 게시글에 대한 직접적인 답글
        ).order_by('-created_at')[:num]

    return comments

def get_num_of_reply_comment(comment: Comment) -> int:
    """
        재귀적 방법으로 'comment'에 대한 답글, 그 답글에 대한 답글, 그 답글에 대한 답글의 답글.........
        들의 수량을 획득하여 리턴

        주의:
        1. recursive function으로 대규모 dataset에선 서버 과부하 가능성 있음 (추후에 optimization 필요)
    """
    cur_replying_comments = Comment.objects.filter(replying_to=comment)
    reply_num = len(cur_replying_comments) # 현재 게시글에 대한 직접적인 답글 갯수
    for c in cur_replying_comments:
        reply_num += get_num_of_reply_comment(c) # 현재 댓글의 답글에 대한 답글 갯수을 각각 모두 획득한 합

    return reply_num

def get_reply_comment(comment: Comment,
                      ts: str,
                      num: int) -> List[Comment]:
    """
        댓글의 답글 획득:
        1. 지정한 댓글 'comment'에 대한
        2. timestamp가 'ts'와 같거나 오래된 (ts가 None일 시 제일 최신의 것들을 리턴)
        3. 'num'개 획득

        주의:
        1. Comments Instance 리스트를 리턴
        2. 'commment' 댓글에 대한 직접적인 답글만 리턴
    """
    if ts: # pagination
        last_seen_datetime = datetime.fromtimestamp(float(ts))
        comments = Comment.objects.filter(
            replying_to=comment, # 게시글에 대한 직접적인 답글
            created_at__lte=last_seen_datetime
            ).order_by('-created_at')[:num]
    else: # 최신 댓글
        comments = Comment.objects.filter(
            replying_to=comment # 게시글에 대한 직접적인 답글
        ).order_by('-created_at')[:num]

    return comments

def get_usercode_list_for_comments_of_post(post: Post) -> Dict:
    """
        지정 게시글 'post'에 댓글 (대댓글 등 모두 포함)을 작성한 모든 사용자를 각 넘버로 매겨 반환.
    """
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    post_author = post.author
    
    # 작성자를 제외한 유저명들 (댓글을 단 시간순으로 정리)
    usernames = [c.author.username for c in comments if c.author.username != post_author.username]
    #unique_usernames = list(set(usernames))

    result_dict={
        post_author.username:0
    }
    cur_count = 1 # 유저 코드
    for name in usernames:
        if name not in result_dict: # 새로 
            result_dict[name] = cur_count
            cur_count += 1

    return result_dict


    