from django.db import models
from django.utils.timezone import localtime
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from boards.models import BaseBoard



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

    # 내용 (text only)
    # TODO: MULTI-MEDIA?
    content=models.TextField(
        blank=False
    )

    # 작성자
    author=models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )

    # 게시판
    board=models.ForeignKey(
        BaseBoard,
        on_delete=models.PROTECT, # Board 삭제 시, 게시물 존재 시 오류 raise
    )

    # 등록 시간
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 가독 created_at
    @property
    def created_at_readable(self):
        return localtime(self.created_at).strftime("%Y-%m-%d %H:%M:%S")

    # 최근 수정 시간
    last_modified = models.DateTimeField(
        auto_now=True
    )

    @property
    def last_modified_readable(self):
        return localtime(self.last_modified).strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        ordering=['created_at']
        verbose_name='게시글'
        verbose_name_plural='게시글들'

    def __str__(self):
        return f'{self.board.name}-{self.title}-{self.created_at_readable}'
    
class PostMedia(models.Model):
    """
        게시글 내 첨부된 Multi-media 관련 모델 (사진/영상)
    """
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE # 포스트 삭제 시 삭제
    )

    url=models.URLField(
        null=False,
        blank=False
    )

    class Meta:
        ordering=['post__created_at']
        verbose_name='게시글 첨부 사진/영상'
        verbose_name_plural='게시글 첨부 사진/영상들'

    def __str__(self):
        return f'{self.post.title}'
    
class UserPostProfile(models.Model):
    """
        유저 관련 기타 정보 저장
        admin 화면에서의 용이한 관리를 위한 모델
    """
    # 관련 유저
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # 유저가 작성한 게시글
    posts=models.ManyToManyField(
        Post
    )

# User모델 생성 시, UserPostProfile 자동 생성
@receiver(post_save, sender=User)
def create_user_post_profile(sender, instance, created, **kwargs):
    if created:
        UserPostProfile.objects.create(user=instance)
# User모델 저장 시, 관련 UserPostProfile 자동 저장
@receiver(post_save, sender=User)
def save_user_post_profile(sender, instance, **kwargs):
    instance.userpostprofile.save()