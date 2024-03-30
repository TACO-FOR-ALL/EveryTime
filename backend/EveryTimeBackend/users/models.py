from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import localtime

import uuid
# Create your models here.

class Organization(models.Model):
    """
        학교/단체 관련 정보를 저장하는 모델.
        명칭/지역을 필수적으로 제공해야 함.
    """
    # 고유 식별 id
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    # 명칭
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        default=''
    )

    # 등록 시간
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 지역 (국가)
    # 먼저 선택사항들을 정의하고 아래 choices에 등록
    # 선택사항:
    S_KOREA = 'KOR'
    CHINA = 'CHN'

    region = models.CharField(
        max_length=16,
        null=False,
        blank=False,
        choices={
            S_KOREA: "대한민국",
            CHINA: "중국"
        },
        default=S_KOREA,
    )

class OrganizationEmail(models.Model):
    """
        학교/단체 인증용 이메일
    """
    # 관련 학교/단체
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )

    # 등록 시간
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 최근 수정 시간
    last_modified = models.DateTimeField(
        auto_now=True
    )

    # Email Address Suffix
    suffix = models.CharField(
        max_length=32,
        unique=True,
        null=False,
        blank=False,
        default='@example.com'
    )

class User(AbstractUser):
    """
        Django에서 제공한 User 모델을 기반으로 확장한 모델.
        username, password을 필수적으로 제공해야 함. (email은 임의적으로 강제)
    """
    # 소속 단체
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT
        # 단체/학교 삭제 시, 만약 해당 단체/학교 소속 유저가 있을 경우 오류 raise
    )

    # 가입 시간
    signup_at = models.DateTimeField(
        auto_now_add=True
    )

    def get_readable_signup_at(self):
        """
            signup_at 필드를 가독성이 좋은 포맷으로 리턴
        """
        readable = localtime(self.signup_at).strftime('%Y-%m-%d %H:%M:%S')
        return readable