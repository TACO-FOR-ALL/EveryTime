from typing import Tuple
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.conf import settings
from EveryTimeBackend.mail_templates import *

def send_auth_email(email_address: str, content: str, type: int) -> Tuple:
    """
        Developer:
        기능: 인증용 이메일을 전송하고 전송 결과를 Tuple로 리턴: True, None: 성공 / False, str: 실패
        Type: 1 - 가입 인증; 2 - 비밀번호 리셋
    """ 
    try:
        subject_template=''
        message_template=''
        if type == 1: # 가입 인증
            subject_template = SIGNUP_SUBJECT
            message_template = SIGNUP_MESSAGE
        elif type == 2: # 비밀번호 리셋 인증
            subject_template = PW_RESET_SUBJECT
            message_template = PW_RESET_MESSAGE
        else: # Unknown Type
            return (False, "실패, Unknown auth type!")

        send_mail(subject=subject_template,
                  message=message_template.format(content=content),
                  from_email=settings.MAIL['default']['EMAIL_HOST_USER'], # TODO: 추후 수정이 필요할 것으로 보임
                  recipient_list=[email_address])
        return (True, None)
    except BadHeaderError:
        return (False, "실패, BadHeaderError!")
    except Exception as e:
        return (False, str(e))