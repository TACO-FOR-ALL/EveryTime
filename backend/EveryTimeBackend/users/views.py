from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.db import transaction
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from .utils import *

from EveryTimeBackend.utils import ResponseContent, generate_auth_code

# class ProtectedTestView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response('Get is good!')
#     def post(self, request):
#         msg = request.data.get('msg')
#         return Response(f'Post got the msg: {msg}')
    
class CustomTokenRefreshView(TokenRefreshView):
    """
        Developer: Macchiato
        API: /users/refresh-access-token
        기능: 가입 가능 학교/단체 리스트 제공
    """
    def post(self, request, *args, **kwargs):
        original_response = super().post(request, *args, **kwargs)
        if original_response.status_code != 200:
            # TODO: LOGGING using original_response.data
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
    def get(self, request):
        try:
            organizations = Organization.objects.all()
            serializer = OrganizationSerializer(organizations, many=True)
            return Response(data=ResponseContent.success(data=serializer.data,
                                                         data_field_name='organizations'))
        except Exception as e: # 서버 에러
            # TODO: LOGGING
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class users_organization_mails_view(APIView):
    """
        Developer: Macchiato
        API: /users/organization/emails
        기능: 선택한 학교/단체에서 인증에 사용할 수 있는 메일 제공
    """
    def post(self, request):
        try:
            org_id_to_use = request.data.get('org_id')

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
            email_serializer = OrganizationEmailListSerializer(org_emails,
                                                               many=True)
            return Response(data=ResponseContent.success(data=email_serializer.data,
                                                         data_field_name='emails'))

        except Exception as e: # 서버 에러
            # TODO: LOGGING
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
    def post(self, request):
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

            # 메일 발송
            cur_auth_code = generate_auth_code()
            send_result, fail_reason = send_auth_email(email_address=email_to_use,
                                                       content=cur_auth_code,
                                                       type=1)
            
            if not send_result:
                # TODO: 인증 메일 발송 실패 LOGGING
                if fail_reason:
                    raise Exception(fail_reason)
                else:
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
            except:
                # TODO: LOGGING
                raise Exception("가입인증메일 관련 DB 조작 실패")
            
            return Response(
                ResponseContent.success()
            )
        except Exception as e: # 서버 에러
            # TODO: LOGGING using str(e)
            print(str(e))
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
    def post(self, request):
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
                obj_EmailAuth.verified = True
                obj_EmailAuth.save()
            except:
                # TODO: LOGGING
                raise Exception("인증 완료 관련 DB 조작 실패")
            
            return Response(ResponseContent.success())
        except Exception as e:
            # TODO: LOGGING using str(e)
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
    def post(self, request):
        try:
            username_to_use = request.data.get('username')
            password_to_use = request.data.get('password')
            email_to_use = request.data.get('email')
            organization_id_to_use = request.data.get('organization')

            if User.objects.filter(username=username_to_use).exists():
                return Response(
                    data=ResponseContent.fail(f"해당 ID: {username_to_use}는 사용 중입니다."),
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
                        organization=obj_org
                    )
                    new_user.set_password(password_to_use)
                    new_user.save()
            except:
                # TODO: LOGGING
                raise Exception("회원 가입 관련 DB 조작 실패") 

            return Response(ResponseContent.success())
        except Exception as e:
            # TODO: LOGGING using str(e)
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
    def post(self, request):
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
            # TODO: LOGGING using str(e)
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
    def post(self, request):
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
            send_result, fail_reason = send_auth_email(email_address=email_to_use,
                                                       content=cur_auth_code,
                                                       type=2)
            
            if not send_result:
                # TODO: 인증 메일 발송 실패 LOGGING
                if fail_reason:
                    raise Exception(fail_reason)
                else:
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
            except:
                # TODO: LOGGING
                raise Exception("가입인증메일 관련 DB 조작 실패")
            
            return Response(ResponseContent.success())
        except:
            # TODO: LOGGING using str(e)
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
    def post(self, request):
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
                obj_EmailAuth.verified = True
                obj_EmailAuth.save()
            except:
                # TODO: LOGGING
                raise Exception("인증 완료 관련 DB 조작 실패")
            
            return Response(ResponseContent.success())

        except:
            # TODO: LOGGING using str(e)
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
    def post(self, request):
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
            except:
                # TODO: LOGGING
                raise Exception("비밀번호 변경 관련 DB 조작 실패") 

            return Response(ResponseContent.success())
            
        except:
            return Response(
                data=ResponseContent.fail("서버 에러!"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )