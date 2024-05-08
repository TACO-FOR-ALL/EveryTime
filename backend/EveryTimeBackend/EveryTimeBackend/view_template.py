from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

class LoginNeededView(APIView):
    """
        로그인이 필요한 API의 Base Class
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_user(self, request: Request):
        jwt_authentication = JWTAuthentication()
        try:
            user, _ = jwt_authentication.authenticate(request)
        except Exception as e:
            # TODO: Logging
            # 인증 실패! raise error
            raise AuthenticationFailed
        
        # 인증 완료, user obj 리턴
        return user