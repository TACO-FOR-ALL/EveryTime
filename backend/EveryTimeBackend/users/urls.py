from django.urls import path

from . import views

"""
    URL prefix: /users/
"""
urlpatterns = [
    path("signup", # 회원가입
         views.users_signup_view, 
         name='users.signup'), 

    path("login",  # 로그인
         views.users_login_view,
         name='users.login'),

     path("reset-password/send_auth_email",  # 비밀번호 리셋용 인증 메일 발송
         views.users_reset_password_send_auth_email_view,
         name='users.reset_password.send_auth_email'),

    path("organization/list", # 가입 가능 학교/단체 리스트
         views.users_organization_list_view,
         name='users.organization.list'),

    path("organization/mails", # 특정 학교/단체 인증 가능 이메일 suffix 리스트
         views.users_organization_mails_view,
         name='users.organization.mails'),

    path("organization/send_auth_email", # 인증 메일 발송
         views.users_organization_send_auth_email_view,
         name='users.organization.send_auth_email'),

     path("organization/check_auth_code", # 인증 코드 대조
         views.users_email_auth_confirm_view,
         name='users.organization.check_auth_code'),
]