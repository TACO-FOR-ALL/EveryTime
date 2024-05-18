def generate_auth_code() -> str:
    """
        Developer: Macchiato
        기능: 100000~999999 사이의 랜덤 숫자를 str의 형식으로 리턴
    """
    import random
    return str(random.randint(100000, 999999))

class ResponseContent(object):
    """
        Developer: Macchiato
        기능: 모든 View Function의 Return을 표준화하기 위한 Class
    """
    @staticmethod
    def success(data=None,
                data_field_name: str="data",
                status_code: int=0):
        if data:
            result = {
                "status": status_code,
                data_field_name: data
            }
        else:
            result = {
                "status", status_code
            }
        return result
    @staticmethod
    def fail(error_msg: str="",
             status_code: int=1):
        return {
            "status": status_code,
            "error_msg": error_msg
        }
    
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .mail_templates import get_html_content
from .mail_config import (
    smtp_port,
    smtp_server,
    sender_email,
    password
)
from typing import Tuple

class EmailConfig:
    def __init__(self):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.password = password

def send_auth_email(receiver_email: str,
                    content: str,
                    type: int) -> Tuple[bool, str]:
    try:
        # 이메일 config
        config = EmailConfig()
        
        # 이메일 msg 구성
        msg = MIMEMultipart()
        msg['From'] = config.sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "북경 커뮤니티 회원가입 인증 안내"
        
        
        html=None
        if type == 1: # 가입 인증
            html = get_html_content(content)
        # TODO: type==2: 비번 리셋
        else:
            raise NotImplementedError
        
        msg.attach(MIMEText(html, 'html'))
    
        # SSL로 발송
        smtp = smtplib.SMTP_SSL(config.smtp_server, config.smtp_port)
        smtp.login(config.sender_email, config.password)
        smtp.sendmail(config.sender_email, receiver_email, msg.as_string())
        smtp.quit() # 발송 후 로그아웃
        
        return True, ''
    except Exception as e: # 발송 실패
        return False, str(e)