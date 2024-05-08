# Generated by Django 5.0.3 on 2024-05-07 18:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_alter_baseboard_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBoardProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_boards', models.ManyToManyField(related_name='favorited_by', to='boards.baseboard')),
                ('main_board', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='set_main_by', to='boards.baseboard')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
