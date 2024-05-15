from django.db import models

from posts.models import Post

class Media(models.Model):
    """
        OSS에 저장한 Media 관련 정보
    """
    # OSS에 저장한 object_key
    object_key=models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )

    # 업로드 완료 여부
    uploaded=models.BooleanField(
        default=False
    )

class PostMedia(Media):
    """
        게시글 내 첨부된 media 관련 모델 (사진/영상)
    """
    # 관련 게시글
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE # 포스트 삭제 시 삭제
    )

    class Meta:
        ordering=['post__created_at']
        verbose_name='게시글 첨부 사진/영상'
        verbose_name_plural='게시글 첨부 사진/영상들'

    def __str__(self):
        return f'{self.post.board.name}-{self.post.title}-{self.post.created_at_readable}'