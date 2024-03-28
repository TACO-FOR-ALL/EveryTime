from django.http import JsonResponse

class ViewReturn(object):
    """
        Developer: 박찬빈
        기능: 모든 View Function의 Return을 표준화하기 위한 Class
    """
    @staticmethod
    def success(content=None, http_code=200):
        return JsonResponse(data=content, status=http_code)

    @staticmethod
    def fail(content=None, http_code=500): # 500: server error
        return JsonResponse(data=content, status=http_code)