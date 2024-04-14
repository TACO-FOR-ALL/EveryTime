from typing import Tuple
from django.core.mail import send_mail
from django.core.mail import BadHeaderError



# email_address = "사용자 이메일 주소"
# content = "-"
subject = "북경 커뮤니티 회원가입 인증 안내"
message = f"{content} 본 이메일은 북경 커뮤니티 이용에 필요한 본인확인 절차를 위해 발송되었습니다.\n" \
          "모바일 애플리케이션에서 상기 코드를 입력한 뒤 회원가입을 완료하여 주시기 바랍니다.\n" \
          "본 메일은 발신 전용 메일로 회신이 불가능합니다. 문의사항이 있으시면 고객센터/아래 연락처를 이용하여 주시기 바랍니다."

def send_auth_email(email_address: str, content: str) -> Tuple:
    """
        Developer:
        기능: 인증용 이메일을 전송하고 전송 결과를 Tuple로 리턴: True, None: 성공 / False, str: 실패
    """
        
    try:
        send_mail(subject, message, email_address, content)
        return (True, None)
    except BadHeaderError:
        return (False, "실패: 메일 제목 혹은 형식에 문제가 있어 전송을 실패했습니다.")
    except Exception as e:
        return (False, str(e))