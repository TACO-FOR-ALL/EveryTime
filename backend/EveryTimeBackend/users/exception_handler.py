from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from EveryTimeBackend.utils import ResponseContent

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    print("Exception handler working! exc instance:")
    print(type(exc))
    # TODO: LOGGING with more detail?
    if isinstance(exc, (TokenError, InvalidToken)): # WARN: InvalidToken is child class of AuthenticationFailed
        return Response(
            data=ResponseContent.fail(error_msg='TOKEN EXPIRED or INVALID',
                                      status_code=3),
            status=status.HTTP_401_UNAUTHORIZED
        )
    # elif isinstance(exc, AuthenticationFailed):
    #     return Response(
    #         data=ResponseContent.fail(error_msg='JWT유저 인증 실패!',
    #                                   status_code=2),
    #         status=status.HTTP_401_UNAUTHORIZED
    #     )
    elif isinstance(exc, NotAuthenticated):
        return Response(
            data=ResponseContent.fail(error_msg='JWT access token 미제공!',
                                      status_code=2),
            status=status.HTTP_401_UNAUTHORIZED
        )

    return response