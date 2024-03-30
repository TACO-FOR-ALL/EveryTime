# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
"""
        *추천 mysql 클라이언트 라이브러리: mysqlclient>=1.4.3
"""
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taco_dev',  # DB 명칭
        'USER': 'root',  # DB 서버 접속 유저 ID
        'PASSWORD': '123456',  # DB서버 접속 유저 PW
        'HOST': '127.0.0.1',  # DB서버 호스트 (로컬일 경우 127.0.0.1)
        'PORT': '3306',  # DB서버 포트
    }
}