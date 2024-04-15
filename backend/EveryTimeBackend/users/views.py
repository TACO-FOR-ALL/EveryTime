import json
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib.auth import authenticate, login
from django.db import transaction

from .models import *
from .utils import send_auth_email

from EveryTimeBackend.utils import ViewReturn

def users_signup_view(request: HttpRequest):
    """
        Developer: Macchiato
        API: /users/signup
        기능: 회원가입
    """
    request_data = json.loads(request.body)
    id_to_use = request_data.get('id')
    pw_to_use = request_data.get('password')
    email_to_use = request_data.get('email')
    organization_id_to_use = request_data.get('organization_id')

    # username 확인
    if User.objects.filter(username=id_to_use).exists():
        resp = {
            "status": 1,
            "error_msg": f"해당 ID: {id_to_use}는 사용 중입니다."
        }
        return ViewReturn.fail(content=resp)
    
    # 학교/단체 확인
    of = Organization.objects.filter(id=organization_id_to_use)
    if len(of) == 0:
        resp = {
            "status": 1,
            "error_msg": f"잘못된 학교/단체 ID: {organization_id_to_use}"
        }
        return ViewReturn.fail(content=resp)
    organization_to_use = of.first()

    # 인증 완료 여부 확인
    email_auth_to_check = EmailAuthentication.objects.filter(obj_email=email_to_use,
                                                             auth_type=EmailAuthentication.SIGNUP).first()
    if email_auth_to_check is None: # 인증 기록 부재
        resp = {
            "status": 1,
            "error_msg": f"해당 ID: {id_to_use}/email: {email_to_use}는 인증을 진행하지 않았거나 인증 완료 후 가입까지의 제한 시간이 경과하였습니다."
        }
        return ViewReturn.fail(content=resp)
    # 인증 완료 시 인증 완료 기록 삭제
    try:
        email_auth_to_check.delete()
    except Exception as e:
        resp = {
            "status": 1,
            "error_msg": "서버 오류!"
        }
        # TODO: LOGGING
        return ViewReturn.fail(content=resp)

    # 가입 진행
    try:
        new_user = User(
            username=id_to_use,
            password=pw_to_use,
            email=email_to_use,
            organization=organization_to_use
        )
        new_user.save()

        resp = {
            "status": 0
        }
        return ViewReturn.success(content=resp)
    except Exception as e:
        resp = {
            "status": 1,
            "error_msg": "서버 오류!"
        }
        # TODO: LOGGING
        return ViewReturn.fail(content=resp)

def users_login_view(request: HttpRequest):
    """
        Developer: 
        API: /users/login
        기능: 로그인
    """
    request_data = json.loads(request.body)
    id_to_use = request_data.get('id')
    pw_to_use = request_data.get('password')
    
    # Authentication
    user = authenticate(username = id_to_use, password = pw_to_use)
    if user is not None:
        if user.is_active:
            login(request, user)        # session에 데이터 저장
            resp = {
                "status" : 0,
                "message" : "로그인 성공"
            }
            return ViewReturn.success(content=resp)
        else:
            resp = {
            "status" : 1,
            "error_msg" : "해당 계정은 비활성화 상태입니다."
        }
        return ViewReturn.fail(content=resp)
    else:
        resp = {
            "status" : 1,
            "error_msg" : "ID 또는 비밀번호가 잘못되었거나 존재하지 않는 계정입니다."
        }
        return ViewReturn.fail(content=resp)

def users_reset_password_send_auth_email_view(request: HttpRequest):
    """
        Developer: 
        API: /users/reset-password/send_auth_email
        기능: 가입 시 사용한 이메일을 받아 비밀번호 리셋용 인증 코드 전송
    """
    # TODO
    raise NotImplementedError


def users_organization_list_view(request: HttpRequest):
    """
        Developer: Macchiato
        API: /users/organization/list
        기능: 가입 가능 학교/단체 리스트 제공
    """
    # 학교/단체 리스트 query
    organizations = Organization.objects.all()
    data = []
    for org in organizations:
        cur_org = {
            "name": org.name,
            "region": org.region,
            "id": org.id
        }
        data.append(cur_org)

    resp = {
        "status": 0,
        "organizations": data
    }
    return ViewReturn.success(content=resp)

def users_organization_mails_view(request: HttpRequest):
    """
        Developer: Macchiato
        API: /users/organization/emails
        기능: 선택한 학교/단체에서 인증에 사용할 수 있는 메일 제공
    """
    # 학교/단체 query
    request_data = json.loads(request.body)
    org_id_to_use = request_data.get('org_id')
    obj_org = Organization.objects.filter(id=org_id_to_use).first()

    # 해당 학교/단체 없음
    if obj_org is None:
        resp = {
            "status": 1,
            "error_msg": "해당 ID를 사용하는 학교/단체가 존재하지 않습니다."
        }
        return ViewReturn.fail(content=resp)

    # 해당 학교/단체 email suffix query
    org_emails = OrganizationEmail.objects.filter(organization=obj_org).all()
    data = [email.suffix for email in org_emails]

    resp = {
        "status": 0,
        "emails": data
    }
    return ViewReturn.success(content=resp)

def users_organization_send_auth_email_view(request: HttpRequest):
    """
        Developer: 
        API: /users/organization/send_auth_email
        기능: 사용자가 제공한 이메일로 인증 메일 발송
    """
    request_data = json.loads(request.body)
    organization_id_to_use = request_data.get('organization_id')
    email_to_use = request_data.get('email')

    conflict_email_user = User.objects.filter(email=email_to_use).first()
    if conflict_email_user is not None:
        resp = {
            "status": 1,
            "error_msg": "해당 이메일은 이미 사용 중입니다."
        }
        return ViewReturn.fail(content=resp)
    
    obj_organization = Organization.objects.filter(id=organization_id_to_use).first()
    if obj_organization is not None:
        resp = {
            "status": 1,
            "error_msg": "잘못된 학교/단체 ID"
        }
        return ViewReturn.fail(content=resp)
    
    obj_email_suffix = '@' + email_to_use.split('@')[1]
    obj_org_email_suffix_list = OrganizationEmail.objects.filter(organization=obj_organization)
    if obj_email_suffix not in obj_org_email_suffix_list:
        resp = {
            "status": 1,
            "error_msg": "해당 이메일은 해당 학교/단체 인증에 사용 가능한 이메일이 아닙니다."
        }
        return ViewReturn.fail(content=resp)

    import random
    cur_auth_code = random.randint(100000, 999999)

    send_result, reason = send_auth_email(email_address=email_to_use,
                                          content=cur_auth_code)
    if not send_result:
        # TODO: 인증 메일 발송 실패 LOGGING
        resp = {
            "status": 1,
            "error_msg": f"서버 오류! 인증 메일 발송 실패"
        }
        return ViewReturn.fail(content=resp)
    
    try:
        with transaction.atomic(): # 민감한 data 삭제는 transaction control
            email_auth_to_delete_list = EmailAuthentication.objects.filter(obj_email=email_to_use,
                                                                           auth_type=EmailAuthentication.SIGNUP)
            for email_to_delete in email_auth_to_delete_list:
                email_to_delete.delete()
        
            cur_email_auth = EmailAuthentication(obj_email=email_to_use,
                                                 auth_code=cur_auth_code,
                                                 auth_type=EmailAuthentication.SIGNUP)
            cur_email_auth.save()
    except Exception as e:
        resp = {
            "status": 1,
            "error_mgs": "인증 메일 처리 중 DB 오류!"
        }
        return ViewReturn.fail(content=resp)

    resp = {
        "status": 0
    }
    return ViewReturn.success(content=resp)
    

def users_email_auth_confirm_view(request: HttpRequest):
    """
        Developer: Macchiato
        API: /users/organization/check_auth_code
        기능: 사용자가 frontend에 입력한 인증코드와 발송한 인증코드 대조
    """
    request_data = json.loads(request.body)
    email_to_check = request_data.get('email')
    code_to_check = request_data.get('code')

    obj_EmailAuth = EmailAuthentication.objects.filter(obj_email=email_to_check,
                                                       auth_type=EmailAuthentication.SIGNUP).first()
    if obj_EmailAuth is None:
        resp = {
            "status": 1,
            "error_msg": f"잘못된 이메일: {email_to_check}, 해당 ID는 인증 요청을 발송하지 않았습니다."
        }
        return ViewReturn.fail(content=resp)
    
    if not obj_EmailAuth.check_auth_code(code_to_check):
        resp = {
            "status": 1,
            "error_msg": f"잘못된 인증코드: {code_to_check}"
        }
        return ViewReturn.fail(content=resp)
    
    try: # 인증 완료
        obj_EmailAuth.verified = True
        obj_EmailAuth.save()
        resp = {
            "status": 0
        }
        return ViewReturn.success(content=resp)
    except Exception as e:
        resp = {
            "status": 1,
            "error_msg": "서버 오류!"
        }
        # TODO: LOGGING
        return ViewReturn.fail(content=resp)