# Generated by Django 5.0.3 on 2024-05-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='clubs',
            field=models.ManyToManyField(blank=True, to='users.club'),
        ),
    ]