from django.db import models

from users.models import Organization, Region, Club

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

    region=models.ForeignKey(
        Region,
        on_delete=models.PROTECT, # 지역 관련 게시판 존재 시 에러
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
        return f'{self.region.name}-{self.name}'

class OrganizationBoard(BaseBoard):
    """
        학교/단체 게시판 모델
    """
    organization=models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering=['created_at']
        verbose_name='학교/단체 게시판'
        verbose_name_plural='학교/단체 게시판들'

    def __str__(self):
        return f'{self.organization.name}-{self.name}'

class ClubBoard(BaseBoard):
    """
        동아리 게시판 모델
    """
    club=models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering=['created_at']
        verbose_name='동아리 게시판'
        verbose_name_plural='동아리 게시판들'

    def __str__(self):
        return f'{self.club.name}-{self.name}'
