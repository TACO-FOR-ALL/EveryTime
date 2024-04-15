# Generated by Django 5.0.3 on 2024-04-14 16:57

import django.db.models.deletion
import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailauthentication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='region',
            field=models.CharField(choices=[('KOR', '대한민국'), ('CHN', '중국'), ('OTH', '기타')], default='CHN', max_length=16),
        ),
        migrations.AlterField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(default=users.models.Organization.get_default_organization, on_delete=django.db.models.deletion.PROTECT, to='users.organization'),
        ),
    ]
