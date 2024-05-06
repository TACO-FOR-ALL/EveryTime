from django.db import models
from users.models import *

class BaseBoard(models.Model):
    """
        게시판 모델
    """
    name=models.CharField(
        max_length=32,
        null=False,
        blank=False,
        unique=False,
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


class Post(models.Model):
    """
        게시글 모델.
    """
    # 제목
    title=models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=False,
        default='SYSTEM'
    )

    # 내용
    # TODO
    #content=models

    # 미리보기 사진 프로필
    profile=models.URLField(
        default='SYSTEM' #
    )

    # 작성자
    author=models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL, # 유저 삭제 시, 작성자=NULL
    )

    board=models.ForeignKey(
        BaseBoard,
        on_delete=models.PROTECT, # Board 삭제 시, 게시물 존재 시 오류 raise
    )

    # 등록 시간
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 최근 수정 시간
    last_modified = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering=['created_at']
        verbose_name='게시글'
        verbose_name_plural='게시글들'

    def __str__(self):
        return f'{self.board.name}-{self.title}-{localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}'