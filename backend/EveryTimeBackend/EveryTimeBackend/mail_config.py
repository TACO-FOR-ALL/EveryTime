
MAIL = {
    'default': {
        'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',  # SMTP 방식 채택
        'EMAIL_HOST': 'smtp.gmail.com',
        'EMAIL_USE_SSL': True,
        'EMAIL_PORT': 465,
        'EMAIL_HOST_USER': '메일 계정의 메일 주소',
        'EMAIL_HOST_PASSWORD': '메일 계정의 pwd'
    }
}