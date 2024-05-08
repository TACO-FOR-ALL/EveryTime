from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import localtime

from datetime import datetime, timedelta

class Region(models.Model):
    """
        국가/지역 모델
    """
    # 지역 (국가)
    # 먼저 선택사항들을 정의하고 아래 choices에 등록
    # 선택사항:
    S_KOREA = 'KOR'
    CHINA = 'CHN'
    OTHERS = 'OTH'

    name=models.CharField(
        max_length=16,
        null=False,
        blank=False,
        choices={
            S_KOREA: "대한민국",
            CHINA: "중국",
            OTHERS: "기타"
        },
        default=OTHERS,
    )
    
    class Meta:
        ordering=['name']
        verbose_name='지역'
        verbose_name_plural='지역들'

    def __str__(self):
        return f'{self.name}'

class Organization(models.Model):
    """
        학교/단체 관련 정보를 저장하는 모델.
        명칭/지역을 필수적으로 제공해야 함.
    """
    # 명칭
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        default='SYSTEM'
    )

    # 등록 시간
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 지역
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering=['created_at']
        verbose_name='학교/단체'
        verbose_name_plural='학교/단체들'

    def __str__(self):
        return f'{self.region.name}-{self.name}'
    
class Club(models.Model):
    """
        동아리 모델
    """
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        default='SYSTEM'
    )

    # 등록 시간
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 지역
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering=['created_at']
        verbose_name='동아리'
        verbose_name_plural='동아리들'

    def __str__(self):
        return f'{self.region.name}-{self.name}'

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
    
    def is_valid(self, valid_time: int=15):
        """
            기능: 발송 후 경과한 시간에 따라 여전히 유효한 인증 기록인지 리턴.
            설명: 유효 기간은 기본 15분이며, call 시 valid_time 설정에 따라 조절 가능
        """
        now = datetime.now(self.sent_at.tzinfo)
        if now > self.sent_at:
            time_diff = now - self.sent_at
            return time_diff <= timedelta(minutes=valid_time)
        else:
            return False
    
    def get_readable_sent_at(self):
        """
            기능: sent_at 필드를 가독성이 좋은 포맷으로 리턴
        """
        readable = localtime(self.sent_at).strftime('%Y-%m-%d %H:%M:%S')
        return readable
    
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
        null=True,
        blank=True,
        default=None
        # 단체/학교 삭제 시, 만약 해당 단체/학교 소속 유저가 있을 경우 오류 raise
    )

    # 가입 시간
    signup_at = models.DateTimeField(
        auto_now_add=True
    )

    # 프로필 다운 url
    profile = models.URLField(
        blank=True,
        default=''
    )

    def get_readable_signup_at(self):
        """
            기능: signup_at 필드를 가독성이 좋은 포맷으로 리턴
        """
        readable = localtime(self.signup_at).strftime('%Y-%m-%d %H:%M:%S')
        return readable
    
    class Meta:
        ordering=['signup_at']
        verbose_name='유저'
        verbose_name_plural='유저들'

    def __str__(self):
        if self.organization:
            return self.organization.region.name + '-' + self.organization.name + '-' + self.username
        else:
            return self.username
        
class UserProfile(models.Model):
    """
        유저 관련 기타 정보 저장:
        1. 소속 동아리
    """
    # 관련 유저
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    clubs=models.ManyToManyField(
        Club
    )

    class Meta:
        ordering=['user__username']
        verbose_name='유저의 동아리 관련 정보'
        verbose_name_plural='유저의 동아리 관련 정보들'

    def __str__(self):
        clubs = ','.join([club.name for club in self.clubs.all()])
            
        return f"""
        {self.user.username}
        -{clubs}
        """
    
# User모델 생성 시, UserBoardProfile 자동 생성
@receiver(post_save, sender=User)
def create_user_board_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
# User모델 저장 시, 관련 UserBoardProfile 자동 저장
@receiver(post_save, sender=User)
def save_user_board_profile(sender, instance, **kwargs):
    instance.userprofile.save()