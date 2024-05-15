# Generated by Django 5.0.3 on 2024-05-15 04:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_rename_userprofile_usercommentprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='like_users',
            field=models.ManyToManyField(related_name='liked_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='replying_to',
            field=models.IntegerField(default=None, null=True),
        ),
    ]