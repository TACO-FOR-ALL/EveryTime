from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, Organization, Region, Club

class BaseBoard(models.Model):
    """
        게시판 모델
    """
    name=models.CharField(
        max_length=32,
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
    region=models.ForeignKey(
        Region,
        on_delete=models.PROTECT, # 지역 관련 게시판 존재 시 에러
    )

    # 전체 공개
    is_public=models.BooleanField(
        default=False
    )

    # 게시판 관리자들
    admins=models.ManyToManyField(
        User,
        blank=True
    )
    
    class Meta:
        ordering=['created_at']
        verbose_name='기본 게시판'
        verbose_name_plural='기본 게시판들'

    def __str__(self):
        return f'{self.name}'
    
class RegionBoard(BaseBoard):
    """
        지역 게시판 모델
    """

    class Meta:
        ordering=['created_at']
        verbose_name='지역 게시판'
        verbose_name_plural='지역 게시판들'

    def __str__(self):
        if self.is_public:
            return f'{self.region.name}-{self.name}-전체 공개'
        else:
            return f'{self.region.name}-{self.name}-전체 비공개'

class OrganizationBoard(BaseBoard):
    """
        학교/단체 게시판 모델
    """
    organization=models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
    )

    # 같은 지역의 유저에게 공개
    is_public_to_region=models.BooleanField(
        default=False
    )

    class Meta:
        ordering=['created_at']
        verbose_name='학교/단체 게시판'
        verbose_name_plural='학교/단체 게시판들'

    def __str__(self):
        all_pub = '전체 공개' if self.is_public else '전체 비공개'
        region_pub = '지역 공개' if self.is_public_to_region else '지역 비공개'
        return f'{self.organization.name}-{self.name}-{all_pub}-{region_pub}'

class ClubBoard(BaseBoard):
    """
        동아리 게시판 모델
    """
    club=models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
    )

    # 같은 지역의 유저에게 공개
    is_public_to_region=models.BooleanField(
        default=False
    )

    class Meta:
        ordering=['created_at']
        verbose_name='동아리 게시판'
        verbose_name_plural='동아리 게시판들'

    def __str__(self):
        all_pub = '전체 공개' if self.is_public else '전체 비공개'
        region_pub = '지역 공개' if self.is_public_to_region else '지역 비공개'
        return f'{self.club.name}-{self.name}-{all_pub}-{region_pub}'

class UserBoardProfile(models.Model):
    """
        유저 관련 기타 정보 저장:
        1. 유저가 설정한 메인 게시판
        2. 유저가 설정한 즐겨찾기 게시판
    """
    # 관련 유저
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    
    # 유저가 설정한 메인 게시판
    main_board=models.ForeignKey(
        BaseBoard,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name='set_main_by'
    )

    # 유저가 즐겨찾기한 게시판
    favorite_boards=models.ManyToManyField(
        BaseBoard,
        blank=True,
        related_name='favorited_by',
    )

    class Meta:
        ordering=['user__username']
        verbose_name='유저의 게시판 관련 정보'
        verbose_name_plural='유저의 게시판 관련 정보들'

    def __str__(self):
        mainboard='None'
        if self.main_board:
            mainboard = self.main_board.name
        favorite_boards = ','.join([board.name for board in self.favorite_boards.all()])
            
        return f"""
        {self.user.username}
        -{mainboard}
        -{favorite_boards}
        """


# User모델 생성 시, UserBoardProfile 자동 생성
@receiver(post_save, sender=User)
def create_user_board_profile(sender, instance, created, **kwargs):
    if created:
        UserBoardProfile.objects.create(user=instance)
# User모델 저장 시, 관련 UserBoardProfile 자동 저장
@receiver(post_save, sender=User)
def save_user_board_profile(sender, instance, **kwargs):
    instance.userboardprofile.save()