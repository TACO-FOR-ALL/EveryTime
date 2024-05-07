from django.db import models

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