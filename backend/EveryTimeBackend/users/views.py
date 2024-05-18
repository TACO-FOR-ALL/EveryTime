from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.db import transaction
from django.contrib.auth import authenticate
from .models import *

from EveryTimeBackend.utils import ResponseContent, generate_auth_code, send_auth_email
from EveryTimeBackend.view_template import LoginNeededView

from loguru import logger
    
class CustomTokenRefreshView(TokenRefreshView):
    """
        Developer: Macchiato
        API: /users/refresh-access-token
        기능: 가입 가능 학교/단체 리스트 제공
    """
    def post(self, request, *args, **kwargs):
        original_response = super().post(request, *args, **kwargs)
        if original_response.status_code != 200:
            logger.debug("JWT Refresh fail, error_data:")
            logger.debug(original_response.data)
            return Response(data=ResponseContent.fail(error_msg='JWT 토큰 갱신 실패!'),
                            status=original_response.status_code)
        else:
            return Response(data=ResponseContent.success(data=original_response.data['access'],
                                                         data_field_name='access'),
                            status=original_response.status_code)
        
class users_organization_list_view(APIView):
    """
        Developer: Macchiato
        API: /users/organization/list
        기능: 가입 가능 학교/단체 리스트 제공
    """
    def get(self, request: Request):
        try:
            organizations = Organization.objects.all()
            result = []
            for org in organizations:
                cur_dict = {
                    "name": org.name,
                    "id": org.id,
                    "region": org.region.name
                }
                result.append(cur_dict)
            return Response(
                data=ResponseContent.success(
                    data=result,
                    data_field_name="organizations"
                )
            )
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class users_organization_mails_view(APIView):
    """
        Developer: Macchiato
        API: /users/organization/emails/?orgid=<org_id>
        기능: 선택한 학교/단체에서 인증에 사용할 수 있는 메일 제공
    """
    def get(self, request: Request):
        try:
            org_id_to_use = request.query_params.get('orgid', None)

            # Request에서 id 미제공
            if org_id_to_use is None:
                return Response(
                    ResponseContent.fail("Request에서 학교/단체 ID을 제공하지 않았습니다."),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            obj_org = Organization.objects.filter(id=org_id_to_use).first()
            # 해당 ID를 사용하는 학교/단체 없음
            if obj_org is None:
                return Response(
                    ResponseContent.fail(f"ID: {org_id_to_use}를 사용하는 학교/단체가 존재하지 않습니다."),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 해당 학교/단체 email suffix query
            org_emails = OrganizationEmail.objects.filter(organization=obj_org).all()
            result = [e.suffix for e in org_emails]
            return Response(data=ResponseContent.success(data=result,
                                                         data_field_name='emails'))

        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("organization id: " + {org_id_to_use})
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class users_organization_send_auth_email_view(APIView):
    """
        Developer: 
        API: /users/organization/send_auth_email
        기능: 사용자가 제공한 이메일로 인증 메일 발송
    """
    def post(self, request: Request):
        try:
            org_id_to_use = request.data.get('organization_id')
            email_to_use = request.data.get('email')

            # Bad Request
            if org_id_to_use is None or email_to_use is None:
                return Response(
                    ResponseContent.fail("Request에서 필요한 모든 정보를 제공하지 않았습니다."),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 사용 중인 이메일
            conflict_email_user = User.objects.filter(email=email_to_use).first()
            if conflict_email_user is not None:
                return Response(
                    ResponseContent.fail(f"{email_to_use}는 사용 중입니다."),
                    status=status.HTTP_409_CONFLICT
                )
            
            obj_organization = Organization.objects.filter(id=org_id_to_use).first()
            if obj_organization is None:
                return Response(
                    ResponseContent.fail(f"제공한 학교/단체 ID: {org_id_to_use}를 사용하는 학교/단체가 존재하지 않습니다."),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            obj_email_suffix = '@' + email_to_use.split('@')[1]
            obj_org_email_list = OrganizationEmail.objects.filter(organization=obj_organization).all()
            suffix_list = [oe.suffix for oe in obj_org_email_list]
            if obj_email_suffix not in suffix_list:
                return Response(
                    ResponseContent.fail(f"제공한 이메일: {email_to_use}는 학교/단체: {obj_organization.name}의 가입에 사용될 수 없습니다."),
                    status=status.HTTP_400_BAD_REQUEST
                )

            # TODO: 마지막 발송 기록 query 후 일정 간격 안에 재발송 요청 금지

            # 메일 발송
            cur_auth_code = generate_auth_code()
            send_result, fail_reason = send_auth_email(receiver_email=email_to_use,
                                                       content=cur_auth_code,
                                                       type=1)
            
            if not send_result:
                if fail_reason:
                    raise Exception(fail_reason)
                else:
                    logger.debug("send_auth_mail() fail but no reason!")
                    logger.debug(f"receiver_mail={email_to_use}, auth_code={cur_auth_code}, type=signup")
                    raise Exception("메일 발송 실패")
            
            try: # 인증 메일 발송 관련 DB 조작
                with transaction.atomic():
                    email_auth_to_delete_list = EmailAuthentication.objects.filter(obj_email=email_to_use,
                                                                                   auth_type=EmailAuthentication.SIGNUP).all()
                    for to_delete in email_auth_to_delete_list:
                        to_delete.delete()
                    
                    cur_email_auth = EmailAuthentication(obj_email=email_to_use,
                                                         auth_code=cur_auth_code,
                                                         auth_type=EmailAuthentication.SIGNUP)
                    cur_email_auth.save()

                    return Response(
                        ResponseContent.success()
                    )
            except Exception as e:
                logger.debug("Error at Email-Auth save")
                logger.debug("email: " + email_to_use)
                raise e
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class users_organization_check_auth_code_view(APIView):
    """
        Developer: Macchiato
        API: /users/organization/check_auth_code
        기능: 사용자가 frontend에 입력한 인증코드와 발송한 인증코드 대조
    """
    def post(self, request: Request):
        try:
            email_to_check = request.data.get('email')
            code_to_check = request.data.get('code')

            # Bad Request
            if email_to_check is None or code_to_check is None:
                return Response(
                    ResponseContent.fail("Request에서 필요한 모든 정보를 제공하지 않았습니다."),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            obj_EmailAuth = EmailAuthentication.objects.filter(obj_email=email_to_check,
                                                       auth_type=EmailAuthentication.SIGNUP).first()
            if obj_EmailAuth is None:
                return Response(
                    ResponseContent.fail(f"{email_to_check} 관련 인증 기록이 없습니다."),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            if not obj_EmailAuth.is_valid():
                return Response(
                    ResponseContent.fail(f"{email_to_check}의 인증 코드가 만료되었습니다."),
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not obj_EmailAuth.check_auth_code(code_to_check):
                return Response(
                    ResponseContent.fail(f"{email_to_check}의 인증코드 {code_to_check}는 틀린 인증코드입니다."),
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            try: # 인증 완료
                with transaction.atomic():
                    obj_EmailAuth.verified = True
                    obj_EmailAuth.save()
                    return Response(ResponseContent.success())
            except Exception as e:
                logger.debug("Error at email auth verify result save")
                logger.debug("Email: " + email_to_check)
                raise e
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class users_signup_view(APIView):
    """
        Developer: Macchiato
        API: /users/signup
        기능: 회원가입
    """
    def post(self, request: Request):
        try:
            username_to_use = request.data.get('username', None)
            password_to_use = request.data.get('password', None)
            nickname_to_use = request.data.get('nickname', None)
            email_to_use = request.data.get('email', None)
            organization_id_to_use = request.data.get('organization_id', None)

            if not (username_to_use and password_to_use and nickname_to_use and email_to_use and organization_id_to_use):
                return Response(
                    data=ResponseContent.fail("필수 파라미터 부재"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(username=username_to_use).exists():
                return Response(
                    data=ResponseContent.fail(f"해당 ID: {username_to_use}는 사용 중입니다."),
                    status=status.HTTP_409_CONFLICT
                )
            if User.objects.filter(nickname=nickname_to_use).exists():
                return Response(
                    data=ResponseContent.fail(f"해당 닉네임: {nickname_to_use}는 사용 중입니다."),
                    status=status.HTTP_409_CONFLICT
                )
            
            obj_org = Organization.objects.filter(id=organization_id_to_use).first()
            if obj_org is None:
                return Response(
                    data=ResponseContent.fail(f"해당 ID: {organization_id_to_use}를 사용하는 학교/단체가 존재하지 않습니다."),
                    status=status.HTTP_404_NOT_FOUND
                )

            email_auth_to_check = EmailAuthentication.objects.filter(obj_email=email_to_use,
                                                                     auth_type=EmailAuthentication.SIGNUP).first()
            if email_auth_to_check is None:
                return Response(
                    data=ResponseContent.fail(f"해당 email: {email_to_use}의 인증 기록이 없습니다."),
                    status=status.HTTP_404_NOT_FOUND
                )
            if not email_auth_to_check.verified:
                return Response(
                    data=ResponseContent.fail(f"해당 email: {email_to_use}의 인증이 완료되지 않았습니다."),
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            try:
                with transaction.atomic():
                    email_auth_to_check.delete()
                    new_user = User(
                        username=username_to_use,
                        email=email_to_use,
                        organization=obj_org,
                        nickname=nickname_to_use
                    )
                    new_user.set_password(password_to_use)
                    new_user.save()
                    return Response(ResponseContent.success())
            except Exception as e:
                logger.debug("Error at create new user")
                raise e
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class users_login_view(APIView):
    """
        Developer: 박시현
        API: /users/login
        기능: 로그인, JWT인증 중 TokenObtainPairView의 역할을 함.
    """
    def post(self, request: Request):
        try:
            username_to_use = request.data.get('username')
            password_to_use = request.data.get('password')

            user = authenticate(username=username_to_use,
                                password=password_to_use)
            # TODO: AUTHENTICATION 불가?
            if user is None:
                return Response(
                    data=ResponseContent.fail(f"ID: {username_to_use} 또는 비밀번호 오류!"),
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.is_active:
                return Response(
                    data=ResponseContent.fail(f"ID: {username_to_use}는 비활성화 상태입니다."),
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # jwt token
            refresh = RefreshToken.for_user(user)
            logger.info(f"Distributed refresh token: {str(refresh)}")
            logger.info(f"Distributed access token: {str(refresh.access_token)}")
            return Response(
                data=ResponseContent.success(
                    data={
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    data_field_name='tokens'
                )
            )
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("requesting_user: " + user.username)
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class users_reset_password_send_auth_email_view(APIView):
    """
        Developer: Macchiato
        API: /users/reset-password/send_auth_email
        기능: 가입 시 사용한 이메일을 받아 비밀번호 리셋용 인증 코드 전송
    """
    def post(self, request: Request):
        try:
            email_to_use = request.data.get('email')

            # Bad Request
            if email_to_use is None:
                return Response(
                    ResponseContent.fail("Request에서 필요한 모든 정보를 제공하지 않았습니다."),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 인증 유저 검색
            email_user = User.objects.filter(email=email_to_use).first()
            if email_user is not None:
                return Response(
                    ResponseContent.fail(f"{email_to_use}을 사용하는 유저가 존재하지 않습니다."),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            cur_auth_code = generate_auth_code()
            send_result, fail_reason = send_auth_email(receiver_email=email_to_use,
                                                       content=cur_auth_code,
                                                       type=2)
            
            if not send_result:
                if fail_reason:
                    raise Exception(fail_reason)
                else:
                    logger.debug("send_auth_mail() fail but no reason!")
                    logger.debug(f"receiver_mail={email_to_use}, auth_code={cur_auth_code}, type=reset-pw")
                    raise Exception("메일 발송 실패")
                
            try: # 인증 메일 발송 관련 DB 조작
                with transaction.atomic():
                    email_auth_to_delete_list = EmailAuthentication.objects.filter(obj_email=email_to_use,
                                                                                   auth_type=EmailAuthentication.PWRESET).all()
                    for to_delete in email_auth_to_delete_list:
                        to_delete.delete()
                    
                    cur_email_auth = EmailAuthentication(obj_email=email_to_use,
                                                         auth_code=cur_auth_code,
                                                         auth_type=EmailAuthentication.PWRESET)
                    cur_email_auth.save()

                    return Response(ResponseContent.success())
            except Exception as e:
                logger.debug("Error at send reset-pw auth mail save")
                logger.debug("Email: " + email_to_use)
                raise e
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class users_reset_password_check_auth_code_view(APIView):
    """
        Developer: Macchiato
        API: /users/reset-password/send_auth_email
        기능: 가입 시 사용한 이메일을 받아 비밀번호 리셋용 인증 코드 전송
    """
    def post(self, request: Request):
        try:
            email_to_check = request.data.get('email')
            code_to_check = request.data.get('code')
            
            # Bad Request
            if email_to_check is None or code_to_check is None:
                return Response(
                    ResponseContent.fail("Request에서 필요한 모든 정보를 제공하지 않았습니다."),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            obj_EmailAuth = EmailAuthentication.objects.filter(obj_email=email_to_check,
                                                       auth_type=EmailAuthentication.PWRESET).first()
            if obj_EmailAuth is None:
                return Response(
                    ResponseContent.fail(f"{email_to_check} 관련 인증 기록이 없습니다."),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            if not obj_EmailAuth.check_auth_code(code_to_check):
                return Response(
                    ResponseContent.fail(f"{email_to_check}의 인증코드 {code_to_check}는 틀린 인증코드입니다."),
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            try: # 인증 완료
                with transaction.atomic():
                    obj_EmailAuth.verified = True
                    obj_EmailAuth.save()
                    return Response(ResponseContent.success())
            except Exception as e:
                logger.debug("Error at reset-pw auth mail result save")
                logger.debug("Email: " + email_to_check)
                raise e

        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class users_reset_password_set_password_view(APIView):
    """
        Developer: Macchiato
        API: /users/reset-password/send_auth_email
        기능: 가입 시 사용한 이메일을 받아 비밀번호 리셋용 인증 코드 전송
    """
    def post(self, request: Request):
        try:
            email_to_use = request.data.get('email')
            password_to_use = request.data.get('password')

            # Bad Request
            if email_to_use is None or password_to_use is None:
                return Response(
                    ResponseContent.fail("Request에서 필요한 모든 정보를 제공하지 않았습니다."),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_to_use = User.objects.filter(email=email_to_use).first()
            if user_to_use is None:
                return Response(
                    data=ResponseContent.fail(f"{email_to_use}를 사용하는 유저는 존재하지 않습니다."),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            email_auth_to_check = EmailAuthentication.objects.filter(obj_email=email_to_use,
                                                                     auth_type=EmailAuthentication.PWRESET).first()
            if email_auth_to_check is None:
                return Response(
                    data=ResponseContent.fail(f"해당 email: {email_to_use}의 인증 기록이 없습니다."),
                    status=status.HTTP_404_NOT_FOUND
                )
            if not email_auth_to_check.verified:
                return Response(
                    data=ResponseContent.fail(f"해당 email: {email_to_use}의 인증이 완료되지 않았습니다."),
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            try:
                with transaction.atomic():
                    email_auth_to_check.delete()
                    user_to_use.set_password(password_to_use)
                    user_to_use.save()

                    return Response(ResponseContent.success())
            except Exception as e:
                logger.debug("Error at reset-pw save")
                logger.debug("Email: " + email_to_use)
                raise e
            
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class users_nickname_view(LoginNeededView):
    """
        Developer: Macchiato
        API: /users/nickname
        기능: 유저 본인의 비익명 게시글 작성 시 노출명 획득 view
    """
    def get(self, request: Request):
        user=self.get_user(request)
        try:
            nickname = user.nickname

            return Response(
                ResponseContent.success(
                    data=nickname,
                    data_field_name='nickname'
                )
            )
        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("requesting_user: " + user.username)
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def post(self, request: Request):
        user=self.get_user(request)
        try:
            nickname_to_use = request.data.get('nickname')
            
            # 필수 파라미터 부재
            if nickname_to_use is None:
                return Response(
                    data=ResponseContent.fail("노출명 미제공!"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 노출명 사용 중
            if User.objects.filter(nickname=nickname_to_use).first():
                return Response(
                    data=ResponseContent.fail(f"해당 노출명: {nickname_to_use}은 사용 중입니다."),
                    status=status.HTTP_400_BAD_REQUEST
                )
        
            try: # 노출명 설정
                with transaction.atomic():
                    user.nickname = nickname_to_use
                    user.save()

                    return Response( # 성공
                        ResponseContent.success()
                    )
            except Exception as e:
                raise e
            

        except Exception as e:
            logger.error("Error at:" + self.__class__.__name__)
            logger.error(str(e))
            logger.debug("requesting_user: " + user.username)
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )