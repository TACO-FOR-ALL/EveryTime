from typing import Tuple
import random
from django.core.mail import send_mail
from .models import SendMail
from django.core.mail import BadHeaderError

def send_auth_email(recipients: str, content: str) -> Tuple:
    """
        Developer:
        기능: 인증용 이메일을 전송하고 전송 결과를 Tuple로 리턴: True, None: 성공 / False, str: 실패
    """

    content = str(random.randint(100000,999999))
    subject = '북경 커뮤니티 회원가입 인증 안내'
    message = '{} 본 이메일은 북경 커뮤니티 이용에 필요한 본인확인 절차를 위해 발송되었습니다.\n \
        모바일 애플리케이션에서 상기 코드를 입력한 뒤 회원가입을 완료하여 주시기 바랍니다.\n \
            본 메일은 발신 전용 메일로 회신이 불가능합니다. 문의사항이 있으시면 고객센터/아래 연락처를 이용하여 주시기 바랍니다.'.format(content)
    sender_email = '발신자 메일'
    recipients = SendMail.objects.values_list('email', flat=True)
        
    try:
        send_mail(subject, message, sender_email, recipients)
        return (True, None)
    except BadHeaderError:
        return (False, "메일 오류")
    except Exception as e:
        return (False, str(e))
