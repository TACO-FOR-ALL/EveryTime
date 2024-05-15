from typing import List, Dict, Any

from posts.models import Post
from .models import PostMedia

import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

def get_oss_callback_payload(prefix: str,
                         id: str,
                         index: str) -> str:
    """
        Media 업로드 시 사용할 callback payload 구성
    """
    return f'key={prefix}/{id}-{index}' # prefix 폴더 내, id-index

def get_oss_callback_api() -> str:
    """
        oss_callback_view에 해당되는 API URL suffix 리턴
    """
    return '/medias/callback'

def get_media_upload_url(key: str) -> str:
    """
        사진/영상 업로드 url을 리턴

        num = 0일 시 빈 리스트 리턴
    """
    # TODO
    raise NotImplementedError
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider()) # OSS_ACCESS_KEY_ID과 OSS_ACCESS_KEY_SECRET 설정 필요
    bucket = oss2.Bucket(auth=auth,
                         endpoint='https://oss-cn-beijing.aliyuncs.com', # TODO
                         bucket_name='' # TODO
    )
    headers=dict() # TODO
    url = bucket.sign_url(method='PUT',
                          key=key,
                          expires=60,
                          slash_safe=True,
                          headers=headers # TODO
    )
    return url

def get_media_download_url(key: str) -> str:
    """
        사진/영상 획득 url 리턴
        
        없을 시 빈 리스트 리턴
    """
    # TODO
    raise NotImplementedError

def get_media_upload_dict(prefix: str,
                          id: int,
                          index: str,
                          obj: Post | Any) -> Dict:
    """
        관련 util 함수들을 활용하여 OSS에서 사용할 object-key를 생성하고
        1. callback_url
        2. callback_payload
        3. upload_url
        을 포함한 Dict를 리턴

        주의: transaction 안전 환경 하에 사용할 것
    """
    result = {
        "callback_url": get_oss_callback_api(),
        "callback_payload": get_oss_callback_payload(prefix=prefix,
                                                     id=str(id),
                                                     index=index)
    }
    key_to_use = result['callback_payload'].split('=')[1], # WARNING: BAD LOGIC
    result['upload_url'] = get_media_upload_url(key=key_to_use)

    # 관련 Media 모델 생성
    # 생성 시 uploaded=False
    if prefix == 'posts':
        new_post_media = PostMedia(
            object_key=key_to_use,
            post=obj
        )
        new_post_media.save()
    else:
        raise Exception(f'알 수 없는 media-prefix: {prefix}')


    return result