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

    # 미리보기 사진 프로필 다운 URL
    profile=models.URLField(
        default='SYSTEM' #
    )

    # 작성자
    author=models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL, # 유저 삭제 시, 작성자=NULL
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
    
class UserPostProfile(models.Model):
    """
        유저 관련 기타 정보 저장
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