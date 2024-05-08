# Generated by Django 5.0.3 on 2024-05-07 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='SYSTEM', max_length=255)),
                ('content', models.TextField()),
                ('profile', models.URLField(default='SYSTEM')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '게시글',
                'verbose_name_plural': '게시글들',
                'ordering': ['created_at'],
            },
        ),
    ]