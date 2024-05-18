from django.urls import path

from . import views

"""
    URL prefix: /users/
"""
urlpatterns = [
#     path("test",
#          views.ProtectedTestView.as_view(),
#          name='users.test'),

    path("signup", # 회원가입
         views.users_signup_view.as_view(), 
         name='users.signup'), 

    path("login",  # 로그인
         views.users_login_view.as_view(),
         name='users.login'),

     path("refresh-access-token", # JWT access token 리프레시
          views.CustomTokenRefreshView.as_view(),
          name='users.refresh_access_token'),

    path("organization/list", # 가입 가능 학교/단체 리스트
         views.users_organization_list_view.as_view(),
         name='users.organization.list'),

    path("organization/emails/", # 특정 학교/단체 가입 인증 가능 이메일 suffix 리스트
         views.users_organization_mails_view.as_view(),
         name='users.organization.mails'),

    path("organization/send_auth_email", # 가입 인증 메일 발송
         views.users_organization_send_auth_email_view.as_view(),
         name='users.organization.send_auth_email'),

     path("organization/check_auth_code", # 가입 인증 코드 확인
         views.users_organization_check_auth_code_view.as_view(),
         name='users.organization.check_auth_code'),

     path("reset-password/send_auth_email",  # 비밀번호 리셋용 인증 메일 발송
         views.users_reset_password_send_auth_email_view.as_view(),
         name='users.reset_password.send_auth_email'),

     path("reset-password/check_auth_code", # 비밀번호 리셋 인증 코드 확인
          views.users_reset_password_check_auth_code_view.as_view(),
          name='users.reset_password.check_auth_code'),

     path("reset-password/set_password", # 비밀번호 리셋
          views.users_reset_password_set_password_view.as_view(),
          name='users.reset_password.set_password'),

     path("nickname",
          views.users_nickname_view.as_view(),
          name='users.nickname')
     
]