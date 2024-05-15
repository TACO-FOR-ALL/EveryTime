from rest_framework.views import APIView
from rest_framework.request import Request

class medias_oss_callback(APIView):
    """
        Developer: Macchiato
        API:
        기능: OSS에서 발송하는 upload success callback 처리
    """
    def post(self, request: Request):
        # TODO: 
        # Post의 경우: 1) 관련 Media.uploaded=True; 2) 관련 Post.pending=False
        raise NotImplementedError