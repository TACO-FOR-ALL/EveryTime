from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import localtime

from users.models import User
from posts.models import Post

class Comment(models.Model):
    """
        댓글 모델
    """
    # 작성자
    author=models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    # 댓글을 단 게시글
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    # 답글일 시, 답한 댓글 (Comment Instance) 의 ID
    # 해당 값이 null일 시, 게시글에 대한 직접적인 댓글
    # ForeignKey 등 Relation의 Integration을 활용할 수 없음으로 사용 시 각별히 주의
    replying_to=models.IntegerField(
        null=True,
        blank=True,
        default=None
    )

    # 삭제 여부 (삭제를 하지 않고 삭제한 댓글로 남김)
    is_deleted=models.BooleanField(
        default=False
    )

    # 등록 시간
    created_at=models.DateTimeField(
        auto_now_add=True
    )

    @property
    def created_at_readable(self):
        return localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')

    # 댓글 내용
    content=models.TextField(
        max_length=1024,
        blank=False
    )

    # 답글에 좋아요를 누른 유저들
    like_users=models.ManyToManyField(
        User,
        related_name='liked_comments',
        blank=True
    )

    class Meta:
        ordering=['created_at']
        verbose_name='댓글'
        verbose_name_plural='댓글들'

    def __str__(self):
        return f'{self.author.username}-{self.post.title}-like:{str(len(self.like_users.all()))}'
        
        
class UserCommentProfile(models.Model):
    """
        유저 관련 기타 정보 저장,
        admin 화면에서의 용이한 관리를 위한 모델
    """
    # 관련 유저
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # 유저가 작성한 댓글
    comments=models.ManyToManyField(
        Comment,
        blank=True
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