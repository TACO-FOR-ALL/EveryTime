# Generated by Django 5.0.3 on 2024-05-06 15:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='baseboard',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.region'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='posts.baseboard'),
        ),
        migrations.AddField(
            model_name='clubboard',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.club'),
        ),
        migrations.AddField(
            model_name='organizationboard',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.organization'),
        ),
    ]
