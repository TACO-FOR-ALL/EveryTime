from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from .models import *

from utils import ViewReturn

def users_signup_view(request: HttpRequest):
    """
        Developer: Macchiato
        API: /users/signup
        기능: 회원가입
    """
    # Request Payload
    id_to_use = request.POST['id']
    pw_to_use = request.POST['password']
    email_to_use = request.POST['email']
    organization_id_to_use = request.POST['organization_id']

    # username 확인
    if User.objects.filter(username=id_to_use).exists():
        content = {
            "status": 1,
            "error_msg": "해당 ID를 사용하는 사용자가 이미 존재합니다."
        }
        return ViewReturn.fail(content=content)
    
    # 학교/단체 확인
    of = Organization.objects.filter(id=organization_id_to_use)
    if len(of) == 0:
        content = {
            "status": 1,
            "error_msg": "해당 ID를 사용하는 학교/단체가 존재하지 않습니다."
        }
        return ViewReturn.fail(content=content)
    organization_to_use = of.first()

    # TODO: should check if email-authentication is done

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
            "error_msg": str(e)
        }
        return ViewReturn.fail(content=resp)


def users_login_view(request: HttpRequest):
    """
        Developer: 
        API: /users/login
        기능: 로그인
    """
    # TODO
    raise NotImplementedError


def users_organization_list_view(request: HttpRequest):
    """
        Developer: 
        API: /users/organization/list
        기능: 가입 가능 학교/단체 리스트 제공
    """
    # TODO
    raise NotImplementedError


def users_organization_mails_view(request: HttpRequest):
    """
        Developer: 
        API: /users/organization/emails
        기능: 선택한 학교/단체에서 인증에 사용할 수 있는 메일 제공
    """
    # TODO
    raise NotImplementedError


def users_organization_send_auth_email_view(request: HttpRequest):
    """
        Developer: 
        API: /users/organization/list
        기능: 사용자가 제공한 이메일로 인증 메일 발송
    """
    # TODO
    raise NotImplementedError