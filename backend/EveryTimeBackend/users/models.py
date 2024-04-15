from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import localtime

import uuid
from datetime import datetime
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
    OTHERS = 'OTH'

    region = models.CharField(
        max_length=16,
        null=False,
        blank=False,
        choices={
            S_KOREA: "대한민국",
            CHINA: "중국",
            OTHERS: "기타"
        },
        default=CHINA,
    )

    @staticmethod
    def get_default_organization():
        """
            시스템 관리에 필요한 default 학교/단체 생성 및 리턴.
        """
        return Organization.objects.get_or_create(name='SYSTEM',
                                                  region=Organization.OTHERS)[0]

    class Meta:
        ordering=['created_at']
        verbose_name='학교/단체'
        verbose_name_plural='학교/단체들'


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

    class Meta:
        ordering=['created_at']
        verbose_name='학교/단체 인증용 이메일 주소'
        verbose_name_plural='학교/단체 인증용 이메일 주소들'

class EmailAuthentication(models.Model):
    """
        모 유저에게 인증용 이메일을 보낼 경우,
        해당 Table에 임시적인 데이터를 저장함.
        BackgroundTask를 통해 정기적인 데이터 청소 필요.
    """
    obj_email = models.EmailField(
        default='taco@example.com',
        null=False,
        blank=False
    )
    
    # 발송한 인증 코드
    auth_code = models.CharField(
        max_length=16,
        null=False,
        blank=False,
    )

    # 이메일 발송 시간
    sent_at = models.DateTimeField(
        auto_now_add=True
    )

    verified = models.BooleanField(
        default=False
    )

    # 인증 유형
    # 먼저 선택사항들을 정의하고 아래 choices에 등록
    # 선택사항:
    SIGNUP = 'signup'
    PWRESET = 'pwreset'

    auth_type = models.CharField(
        max_length=16,
        null=False,
        blank=False,
        choices={
            SIGNUP: "회원가입",
            PWRESET: "비밀번호리셋"
        },
        default=SIGNUP,
    )

    def get_auth_type(self):
        """
            기능: 이메일 인증 유형 제공
        """
        return self.auth_type

    def time_diff(self):
        """
            기능: 발송 후 경과한 시간을 계산하여 제공
        """
        now = datetime.now(self.sent_at.tzinfo)
        diff = now - self.sent_at
        return diff
    
    def check_auth_code(self, code_to_check: str):
        """
            기능: 발송한 인증 코드와 대조하여, 일치할 시 True를 리턴
        """
        return self.auth_code == code_to_check
    
    class Meta:
        ordering=['sent_at']
        verbose_name='가입 인증 메일 발송 기록'
        verbose_name_plural='가입 인증 메일 발송 기록들'


class User(AbstractUser):
    """
        Django에서 제공한 User 모델을 기반으로 확장한 모델.
        username, password을 필수적으로 제공해야 함. (email은 임의적으로 강제)
    """
    # 소속 단체
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        default=Organization.get_default_organization
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
    
    class Meta:
        ordering=['signup_at']
        verbose_name='유저'
        verbose_name_plural='유저들'