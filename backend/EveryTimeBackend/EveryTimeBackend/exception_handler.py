from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from EveryTimeBackend.utils import ResponseContent

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        return Response(
            data=ResponseContent.fail(error_msg='JWT유저 인증 실패!',
                                      status_code=2),
            status=status.HTTP_401_UNAUTHORIZED
        )
    elif isinstance(exc, (TokenError, InvalidToken)):
        return Response(
            data=ResponseContent.fail(error_msg='JWT유저 인증 token 오류!',
                                      status_code=2),
            status=status.HTTP_401_UNAUTHORIZED
        )

    return response