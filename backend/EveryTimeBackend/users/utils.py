import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mail_templates import get_html_content
import mail_config

class EmailConfig:
    def __init__(self):
        self.smtp_server = mail_config.smtp_server
        self.smtp_port = mail_config.smtp_port
        self.sender_email = mail_config.sender_email
        self.password = mail_config.password

def send_auth_email(receiver_email, content):
    config = EmailConfig()
    
    msg = MIMEMultipart()
    msg['From'] = config.sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "북경 커뮤니티 회원가입 인증 안내"
    
    html = get_html_content(content)
    msg.attach(MIMEText(html, 'html'))
    
    try:
        smtp = smtplib.SMTP_SSL(config.smtp_server, config.smtp_port)
        smtp.login(config.sender_email, config.password)
        smtp.sendmail(config.sender_email, receiver_email, msg.as_string())
        smtp.quit()
        print("이메일이 성공적으로 발송되었습니다.")
    except Exception as e:
        print(f"이메일 발송 실패: {e}")
