# Generated by Django 5.0.3 on 2024-05-15 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_alter_comment_like_users_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='replying_to',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
