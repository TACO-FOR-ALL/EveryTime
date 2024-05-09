from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import localtime

from users.models import User
from posts.models import Post

# TODO: 답글?

class Comment(models.Model):
    """
        댓글 모델
    """
    # 작성자
    author=models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )

    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    # 등록 시간
    created_at=models.DateTimeField(
        auto_now_add=True
    )

    @property
    def created_at_readable(self):
        return localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')

    # 댓글 내용
    # TODO: MULTI-MEDIA?
    content=models.TextField(
        max_length=1024,
        blank=False
    )

    class Meta:
        ordering=['created_at']
        verbose_name='댓글'
        verbose_name_plural='댓글들'

    def __str__(self):
        if self.author:
            return f'{self.author.username}-{self.post.title}'
        
class UserCommentProfile(models.Model):
    """
        유저 관련 기타 정보 저장
    """
    # 관련 유저
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # 유저가 작성한 댓글
    comments=models.ManyToManyField(
        Comment
    )

# User모델 생성 시, UserCommentProfile 자동 생성
@receiver(post_save, sender=User)
def create_user_comment_profile(sender, instance, created, **kwargs):
    if created:
        UserCommentProfile.objects.create(user=instance)
# User모델 저장 시, 관련 UserCommentProfile 자동 저장
@receiver(post_save, sender=User)
def save_user_comment_profile(sender, instance, **kwargs):
    instance.usercommentprofile.save()